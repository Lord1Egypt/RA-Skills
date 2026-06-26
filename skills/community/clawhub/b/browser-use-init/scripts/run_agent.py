"""
run_agent.py - 用 browser-use Agent 连接 CDP Chrome 执行任务

环境变量配置:
    CDP_PORT        CDP 调试端口（默认 9222）
    OLLAMA_HOST     Ollama 服务地址（默认 http://localhost:11434）

用法:
    python run_agent.py --task "打开网站搜索信息" [--model qwen3.5:9b] [--port 9222]

依赖:
    pip install browser-use langchain-ollama playwright
    playwright install chromium
    # 确保 Ollama 服务运行中
"""

import asyncio, sys, io, urllib.request, json, argparse, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

DEFAULT_PORT = int(os.getenv("CDP_PORT", "9222"))


def get_cdp_ws_url(port=9222):
    resp = urllib.request.urlopen(f"http://localhost:{port}/json/version", timeout=3)
    data = json.loads(resp.read())
    return data["webSocketDebuggerUrl"]


async def run_task(task: str, model: str = "qwen3.5:9b", port: int = 9222):
    from browser_use import Agent, Browser, BrowserProfile
    from langchain_ollama import ChatOllama

    try:
        ws_url = get_cdp_ws_url(port)
        print(f"[CDP] 已连接 Chrome")
    except Exception as e:
        print(f"[CDP] 不在线: {e}")
        print("请先运行 start_chrome.py 启动 Chrome")
        return

    browser = Browser(
        browser_profile=BrowserProfile(
            cdp_url=ws_url,
            headless=False,
        )
    )

    llm = ChatOllama(model=model)

    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
    )

    print(f"[Agent] 任务: {task}")
    print(f"[Agent] 模型: {model}\n")
    result = await agent.run(max_steps=20)
    print("\n========== 执行结果 ==========")
    print(result)
    print("==============================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="用 browser-use Agent 执行浏览器自动化任务")
    parser.add_argument("--task", required=True, help="要执行的任务描述（自然语言）")
    parser.add_argument("--model", default="qwen3.5:9b", 
                       help="Ollama 模型名称（默认 qwen3.5:9b）")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                       help=f"CDP 调试端口（默认来自 $CDP_PORT 环境变量或 {DEFAULT_PORT}）")
    args = parser.parse_args()

    asyncio.run(run_task(args.task, args.model, args.port))
