#!/usr/bin/env python3
"""
gangtise-kb技能包装器
由于主程序是二进制文件，此脚本作为适配器
"""

import sys
import json
import subprocess
import os
from pathlib import Path

def main():
    """主函数：读取标准输入，调用gangtise-kb二进制程序"""
    try:
        # 读取标准输入
        input_data = sys.stdin.read().strip()
        if not input_data:
            print(json.dumps({"error": "No input provided"}, ensure_ascii=False))
            return
        
        # 解析输入
        params = json.loads(input_data)
        
        # 获取二进制文件路径
        script_dir = Path(__file__).parent
        binary_path = script_dir / "gangtise-kb" / "gangtise-kb.py"
        
        if not binary_path.exists():
            print(json.dumps({"error": f"Binary not found at {binary_path}"}, ensure_ascii=False))
            return
        
        # 构建命令参数
        # 根据输入action决定调用方式
        action = params.get("action", "query")
        
        # 将输入转换为二进制程序能理解的格式
        # 这里需要根据实际二进制程序的接口调整
        
        # 临时方案：尝试运行二进制并传递JSON
        try:
            # 将输入写入临时文件
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(params, f, ensure_ascii=False)
                temp_file = f.name
            
            # 尝试运行二进制
            cmd = [str(binary_path), "--input", temp_file]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # 清理临时文件
            os.unlink(temp_file)
            
            if result.returncode == 0:
                # 尝试解析输出为JSON
                try:
                    output = json.loads(result.stdout)
                    print(json.dumps(output, ensure_ascii=False))
                except json.JSONDecodeError:
                    # 如果不是JSON，返回原始输出
                    print(json.dumps({
                        "result": result.stdout,
                        "raw_output": True
                    }, ensure_ascii=False))
            else:
                print(json.dumps({
                    "error": f"Binary execution failed (code {result.returncode})",
                    "stderr": result.stderr[:500]
                }, ensure_ascii=False))
                
        except subprocess.TimeoutExpired:
            print(json.dumps({"error": "Execution timeout"}, ensure_ascii=False))
        except Exception as e:
            print(json.dumps({"error": f"Execution error: {str(e)}"}, ensure_ascii=False))
            
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {str(e)}"}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": f"Unexpected error: {str(e)}"}, ensure_ascii=False}))

if __name__ == "__main__":
    main()