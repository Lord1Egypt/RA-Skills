#!/usr/bin/env python3
import sys
import os
import subprocess
import tempfile
import json
import shutil
import re

# 限制子进程资源的函数（防止恶意或死循环代码拖垮服务器）
def set_limits():
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    except Exception:
        pass

def compile_cpp(src_path, output_exe, include_path="."):
    cmd = ["g++", "-O2", "-std=c++14", "-I", include_path, src_path, "-o", output_exe]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            return False, result.stderr
        return True, ""
    except subprocess.TimeoutExpired:
        return False, "编译超时 (Timeout)"
    except Exception as e:
        return False, str(e)

def process_samples(problem_md_path, valid_exe, std_exe, run_kwargs, tmpdir):
    """扫描 Markdown 中的样例输入，调用校验器和标程，动态计算并替换输出占位符"""
    if not os.path.exists(problem_md_path):
        return

    with open(problem_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取所有 ```input\n内容\n``` 的代码块
    inputs = re.findall(r'```input\n(.*?)\n```', content, re.DOTALL)
    
    for i, inp_text in enumerate(inputs, start=1):
        placeholder = f"{{{{SAMPLE_OUT_{i}}}}}"
        # 如果题面里没有对应的占位符，跳过
        if placeholder not in content:
            continue

        in_file = os.path.join(tmpdir, f"sample_temp_{i}.in")
        with open(in_file, 'w', encoding='utf-8') as f:
            f.write(inp_text)

        # 1. 喂给 valid 校验输入合法性
        with open(in_file, 'r') as fin:
            v_res = subprocess.run([valid_exe], stdin=fin, capture_output=True, **run_kwargs)
            if v_res.returncode != 0:
                raise Exception(f"AI 编造的样例输入 {i} 格式不合法，未通过校验器:\n{v_res.stderr or v_res.stdout}")

        # 2. 喂给 std 计算真实输出
        with open(in_file, 'r') as fin:
            s_res = subprocess.run([std_exe], stdin=fin, capture_output=True, **run_kwargs)
            if s_res.returncode != 0:
                raise Exception(f"标程运行 AI 样例 {i} 时崩溃:\n{s_res.stderr}")

        # 3. 替换占位符
        out_text = s_res.stdout.strip()
        content = content.replace(placeholder, out_text)

    # 写回文件
    with open(problem_md_path, 'w', encoding='utf-8') as f:
        f.write(content)

def build_fps_xml_and_meta(archive_dir, testdata_dir, problem_md_path, std_cpp_path, total_cases, zip_filename):
    """提取标签，构建 FPS XML 并在工作区生成 meta.json"""

    if not os.path.exists(problem_md_path):
        raise FileNotFoundError(f"找不到题面文件: {problem_md_path}。请检查 AI 是否正确生成了题面。")

    # 1. 读取题面
    with open(problem_md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 尝试提取标题和标签
    title_match = re.search(r'# (.*?)\n', md_content)
    title = title_match.group(1).strip() if title_match else "AI 自动生成题目"

    tags_match = re.search(r'【知识点标签】[：:]\s*(.*)', md_content)
    tags = [t.strip() for t in tags_match.group(1).split(',')] if tags_match else ["未分类"]

    # 2. 组装 FPS XML 字符串 (全程使用 CDATA 保护内容)
    xml_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<fps version="1.2" url="https://github.com/zhblue/freeproblemset">',
            '\t<item>',
            f'\t\t<title><![CDATA[{title}]]></title>',
            '\t\t<time_limit unit="s"><![CDATA[1]]></time_limit>',
            '\t\t<memory_limit unit="mb"><![CDATA[256]]></memory_limit>',
            f'\t\t<description><![CDATA[{md_content}]]></description>'
        ]

    # 3. 嵌入所有测试数据 (Inline)
    for idx in range(1, total_cases + 1):
        in_file = os.path.join(testdata_dir, f"{idx}.in")
        out_file = os.path.join(testdata_dir, f"{idx}.out")
        if os.path.exists(in_file) and os.path.exists(out_file):
            with open(in_file, 'r', encoding='utf-8') as fin:
                xml_parts.append(f'\t\t<test_input><![CDATA[{fin.read()}]]></test_input>')
            with open(out_file, 'r', encoding='utf-8') as fout:
                xml_parts.append(f'\t\t<test_output><![CDATA[{fout.read()}]]></test_output>')

    # 4. 嵌入标程
    with open(std_cpp_path, 'r', encoding='utf-8') as f:
        std_code = f.read()
    xml_parts.append(f'\t\t<solution language="C++"><![CDATA[{std_code}]]></solution>')

    xml_parts.extend(['\t</item>', '</fps>'])

    # 5. 将 problem.xml 写入打包目录中
    xml_path = os.path.join(archive_dir, "problem.xml")
    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(xml_parts))

    # 6. 在当前工作区根目录落盘 meta.json (供外层的 fk-luogu 抓取)
    meta_data = {
        "title": title,
        "tags": tags,
        "zip_path": zip_filename + ".zip"
    }
    meta_path = os.path.join(os.getcwd(), "meta.json")
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta_data, f, ensure_ascii=False, indent=2)

def main():
    # 至少需要 4 个文件参数
    if len(sys.argv) < 5:
        print(json.dumps({"status": "error", "message": "用法: python3 generate.py <gen_cpp> <valid_cpp> <std_cpp> <problem_md> [subtask1点数] [subtask2点数] ..."}))
        sys.exit(1)

    gen_cpp, valid_cpp, std_cpp, problem_md = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    gen_cpp = sys.argv[1].replace('\\', '/')
    valid_cpp = sys.argv[2].replace('\\', '/')
    std_cpp = sys.argv[3].replace('\\', '/')
    problem_md = sys.argv[4].replace('\\', '/')

    # 【核心修复】：解析不定长参数，实现不均匀分配
    if len(sys.argv) > 5:
        try:
            subtask_distribution = [int(x.strip().strip('"').strip("'")) for x in sys.argv[5:]]
        except ValueError:
            # 遇到非法参数时，兜底采用 4-3-3 黄金比例
            subtask_distribution = [4, 3, 3] 
    else:
        # 默认不传参数时，直接采用 4-3-3 黄金比例
        subtask_distribution = [4, 3, 3]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    testlib_src = os.path.join(script_dir, "testlib.h")

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            archive_dir = os.path.join(tmpdir, "archive")
            os.makedirs(archive_dir, exist_ok=True)
            
            shutil.copy2(gen_cpp, os.path.join(archive_dir, "gen.cpp"))
            shutil.copy2(valid_cpp, os.path.join(archive_dir, "valid.cpp"))
            shutil.copy2(std_cpp, os.path.join(archive_dir, "std.cpp"))
            if os.path.exists(problem_md):
                shutil.copy2(problem_md, os.path.join(archive_dir, "problem.md"))
            
            shutil.copy2(testlib_src, os.path.join(tmpdir, "testlib.h"))
            
            gen_exe = os.path.join(tmpdir, "gen")
            valid_exe = os.path.join(tmpdir, "valid")
            std_exe = os.path.join(tmpdir, "std")

            for name, src, exe in [("生成器(gen)", gen_cpp, gen_exe), 
                                   ("校验器(valid)", valid_cpp, valid_exe), 
                                   ("标程(std)", std_cpp, std_exe)]:
                ok, err = compile_cpp(src, exe, include_path=tmpdir)
                if not ok:
                    print(json.dumps({"status": "error", "message": f"{name} 编译失败:\n{err}"}))
                    return

            testdata_dir = os.path.join(archive_dir, "testdata")
            os.makedirs(testdata_dir, exist_ok=True)

            # 【核心修复】：遍历 distribution 数组生成数据
            idx = 1

            run_kwargs = {"text": True, "timeout": 5}
            if sys.platform != "win32":
                run_kwargs["preexec_fn"] = set_limits

            for subtask_id, cases_count in enumerate(subtask_distribution, start=1):
                for tc in range(1, cases_count + 1):
                    in_file = os.path.join(testdata_dir, f"{idx}.in")
                    out_file = os.path.join(testdata_dir, f"{idx}.out")
                    
                    # a. 运行 gen 生成 .in
                    with open(in_file, 'w') as fin:
                        cmd_gen = [gen_exe, str(subtask_id), str(tc)]
                        res = subprocess.run(cmd_gen, stdout=fin, stderr=subprocess.PIPE, 
                                             **run_kwargs)
                        if res.returncode != 0:
                            print(json.dumps({"status": "error", "message": f"生成器在 Subtask {subtask_id} Case {tc} 崩溃:\n{res.stderr}"}))
                            return
                    
                    # b. 运行 valid 校验 .in
                    with open(in_file, 'r') as fin:
                        res = subprocess.run([valid_exe], stdin=fin, capture_output=True, 
                                             **run_kwargs)
                        if res.returncode != 0:
                            print(json.dumps({"status": "error", "message": f"数据校验失败 (Subtask {subtask_id} Case {tc}):\n{res.stderr or res.stdout}"}))
                            return
                    
                    # c. 运行 std 生成 .out
                    with open(in_file, 'r') as fin, open(out_file, 'w') as fout:
                        res = subprocess.run([std_exe], stdin=fin, stdout=fout, stderr=subprocess.PIPE, 
                                             **run_kwargs)
                        if res.returncode != 0:
                            print(json.dumps({"status": "error", "message": f"标程运行失败 (Subtask {subtask_id} Case {tc}):\n{res.stderr}"}))
                            return
                    idx += 1

            student_dir = os.path.join(archive_dir, "student_downloads")
            os.makedirs(student_dir, exist_ok=True)
            
            # 策略：前2组调用 Subtask 1 生成小数据，第3组调用最后一个 Subtask 生成大数据
            student_tasks = [
                (1, 1), # (Subtask编号, 文件编号)
                (1, 2),
                (len(subtask_distribution), 3) 
            ]

            for s_id, file_idx in student_tasks:
                s_in = os.path.join(student_dir, f"sample_test_{file_idx}.in")
                s_out = os.path.join(student_dir, f"sample_test_{file_idx}.out")
                
                # 为防止随机种子与线上数据冲突，给 tc 传参加一个偏移量(如 100)
                with open(s_in, 'w') as fin:
                    res = subprocess.run([gen_exe, str(s_id), str(file_idx + 100)], stdout=fin, stderr=subprocess.PIPE, **run_kwargs)
                    if res.returncode != 0:
                        raise Exception(f"生成线下学生数据(输入)失败: {res.stderr}")
                with open(s_in, 'r') as fin, open(s_out, 'w') as fout:
                    res = subprocess.run([std_exe], stdin=fin, stdout=fout, stderr=subprocess.PIPE, **run_kwargs)
                    if res.returncode != 0:
                        raise Exception(f"生成线下学生数据(输出)失败: {res.stderr}")    


            zip_filename = f"problem_package_{os.urandom(4).hex()}"
            
            try:
                process_samples(os.path.join(archive_dir, "problem.md"), valid_exe, std_exe, run_kwargs, tmpdir)
            except Exception as e:
                print(json.dumps({"status": "error", "message": str(e)}))
                return

            build_fps_xml_and_meta(
                archive_dir=archive_dir,
                testdata_dir=testdata_dir,
                problem_md_path=os.path.join(archive_dir, "problem.md"),
                std_cpp_path=os.path.join(archive_dir, "std.cpp"),
                total_cases=sum(subtask_distribution),
                zip_filename=zip_filename
            )
            
            zip_path = os.path.join(os.getcwd(), zip_filename) 
            shutil.make_archive(zip_path, 'zip', archive_dir)
            final_zip_path = zip_path + ".zip"

            # 兜底清理机制
            source_dir = os.path.dirname(os.path.abspath(gen_cpp))
            if os.path.basename(source_dir) == "problem_temp":
                shutil.rmtree(source_dir, ignore_errors=True)

            print(json.dumps({
                "status": "success", 
                "message": "题目全套包（含题面、源码、测试数据）已成功生成并打包。",
                "zip_path": final_zip_path,
                "total_cases": sum(subtask_distribution)
            }))

        except Exception as e:
            print(json.dumps({"status": "error", "message": f"系统内部错误: {str(e)}"}))

if __name__ == "__main__":
    main()