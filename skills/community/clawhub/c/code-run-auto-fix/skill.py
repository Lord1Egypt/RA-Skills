import subprocess
import tempfile
import os
import asyncio
from mcp.server import Server
import clawhub.llm

server = Server("code-auto-fix")

def safe_run(cmd, timeout=10):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False
        )
        return result.stdout, result.stderr
    except Exception:
        return "", "execution error"

async def fix_code(code: str, error: str, lang: str):
    prompt = f"""你是专业代码修复专家，只输出修复后的完整代码，不要解释，不要多余内容。
语言：{lang}
错误信息：{error}
需要修复的代码：
{code}
"""
    try:
        return await clawhub.llm.generate(prompt=prompt)
    except Exception:
        return code

async def auto_run_and_fix(code: str, lang: str, run_func):
    current_code = code
    out, err = run_func(current_code)

    if err or "ERROR" in out:
        current_code = await fix_code(current_code, err, lang)
        out, err = run_func(current_code)

    return current_code

@server.tool()
async def run_python(code: str) -> str:
    def run(c):
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            f.write(c.encode())
        try:
            return safe_run(["python3", f.name])
        finally:
            os.unlink(f.name)
    return await auto_run_and_fix(code, "python", run)

@server.tool()
async def run_c(code: str) -> str:
    def run(c):
        with tempfile.NamedTemporaryFile(suffix=".c", delete=False) as f:
            f.write(c.encode())
        ex = f.name + ".out"
        try:
            _, compile_err = safe_run(["gcc", f.name, "-o", ex])
            if compile_err:
                return "", compile_err
            return safe_run([ex])
        finally:
            if os.path.exists(ex):
                os.unlink(ex)
            os.unlink(f.name)
    return await auto_run_and_fix(code, "c", run)

@server.tool()
async def run_assembly(code: str) -> str:
    def run(c):
        with tempfile.NamedTemporaryFile(suffix=".asm", delete=False) as f:
            f.write(c.encode())
        o = f.name + ".o"
        ex = f.name + ".out"
        try:
            _, asm_err = safe_run(["nasm", "-f", "elf64", f.name, "-o", o])
            if asm_err:
                return "", asm_err
            _, link_err = safe_run(["ld", o, "-o", ex])
            if link_err:
                return "", link_err
            return safe_run([ex])
        finally:
            for p in [o, ex]:
                if os.path.exists(p):
                    os.unlink(p)
            os.unlink(f.name)
    return await auto_run_and_fix(code, "assembly", run)

if __name__ == "__main__":
    asyncio.run(server.run_stdio_forever())