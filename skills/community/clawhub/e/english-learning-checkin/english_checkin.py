#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
English Learning Check-in Skill
每日英语学习打卡工具
"""

import os
import sys
import json
import platform
import subprocess
import datetime
from pathlib import Path

# 当前 Skill 版本
SKILL_VERSION = "1.0.0"

# 设置输出编码为 UTF-8（Windows 兼容）
if platform.system() == "Windows":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 技能目录和数据目录（使用相对路径）
SKILL_DIR = Path(__file__).parent.resolve()
DATA_DIR = SKILL_DIR / "data"
CONFIG_FILE = DATA_DIR / "config.json"
QUOTES_USED_FILE = DATA_DIR / "quotes_used.json"


def ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_json(file_path, default=None):
    """加载 JSON 文件"""
    if default is None:
        default = {}
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return default


def save_json(file_path, data):
    """保存 JSON 文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_used_quotes():
    """获取已使用的名言列表"""
    ensure_data_dir()
    return load_json(QUOTES_USED_FILE, [])


def save_used_quotes(quotes):
    """保存已使用的名言列表"""
    ensure_data_dir()
    save_json(QUOTES_USED_FILE, quotes)


# 全局变量存储 learning-checkin 路径
_LEARNING_CHECKIN_PATH = None


def parse_global_args():
    """解析全局参数"""
    global _LEARNING_CHECKIN_PATH
    
    # 优先从环境变量读取
    env_path = os.environ.get("LEARNING_CHECKIN_PATH")
    if env_path:
        script_path = Path(env_path)
        if script_path.exists():
            _LEARNING_CHECKIN_PATH = script_path
            return
    
    # 从命令行参数读取（--learning-checkin-path 必须在命令之前）
    # 例如: python english_checkin.py --learning-checkin-path /path/to/script.py checkin
    new_argv = []
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--learning-checkin-path" and i + 1 < len(sys.argv):
            script_path = Path(sys.argv[i + 1])
            if script_path.exists():
                _LEARNING_CHECKIN_PATH = script_path
            i += 2
        else:
            new_argv.append(arg)
            i += 1
    
    # 更新 sys.argv，移除全局参数
    sys.argv = [sys.argv[0]] + new_argv


def get_learning_checkin_script():
    """获取 learning-checkin 脚本路径"""
    global _LEARNING_CHECKIN_PATH
    
    if _LEARNING_CHECKIN_PATH and _LEARNING_CHECKIN_PATH.exists():
        return _LEARNING_CHECKIN_PATH
    
    # 尝试在当前目录下查找
    local_path = SKILL_DIR / "learning-checkin" / "learning_checkin.py"
    if local_path.exists():
        return local_path
    
    return None


def init_learning_checkin():
    """初始化 learning-checkin"""
    script_path = get_learning_checkin_script()
    if not script_path or not script_path.exists():
        return None, "learning-checkin 未安装，请先安装 learning-checkin skill"
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), "init"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30
        )
        if result.returncode == 0:
            try:
                return json.loads(result.stdout), "success"
            except:
                return {"message": result.stdout}, "success"
        else:
            return None, result.stderr
    except Exception as e:
        return None, str(e)


def run_learning_checkin_command(command):
    """运行 learning-checkin 命令"""
    script_path = get_learning_checkin_script()
    if not script_path or not script_path.exists():
        return None, "learning-checkin 未安装"
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), command],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30
        )
        if result.returncode == 0:
            try:
                return json.loads(result.stdout), "success"
            except:
                return {"message": result.stdout}, "success"
        else:
            return None, result.stderr
    except Exception as e:
        return None, str(e)


def check_learning_checkin():
    """检查 learning-checkin 是否可用"""
    script_path = get_learning_checkin_script()
    return script_path is not None and script_path.exists()


def handle_init():
    """处理初始化"""
    ensure_data_dir()
    
    # 检查 learning-checkin 是否安装
    if not check_learning_checkin():
        return {
            "require_install": True,
            "message": "需要先安装 learning-checkin 依赖",
            "install_url": "https://clawhub.ai/daizongyu/learning-checkin",
            "hint": "安装后请使用 --learning-checkin-path 参数指定 learning_checkin.py 的路径"
        }
    
    # 初始化 learning-checkin
    data, status = init_learning_checkin()
    
    # 创建默认配置
    config = load_json(CONFIG_FILE, {})
    if "learning_type" not in config:
        config["learning_type"] = "general"
        config["created_at"] = datetime.datetime.now().isoformat()
        save_json(CONFIG_FILE, config)
    
    # 获取已使用的名言
    used_quotes = get_used_quotes()
    
    welcome_message = f"""欢迎使用每日英语学习打卡！

每天坚持学习英语，日积月累才能取得进步。
现在请开始你的英语学习之旅吧！

请告诉我你今天学习的英语内容是什么？（如：托福、雅思、PET、新概念等）
或者直接说"我已完成学习"进行打卡。

注意：每日英语名言将由我为你自动生成，确保每天的名言都不重复。"""
    
    return {
        "welcome_message": welcome_message,
        "learning_checkin_init": data if data else {},
        "used_quotes_count": len(used_quotes)
    }


def handle_checkin(learning_type=None):
    """处理打卡"""
    ensure_data_dir()
    
    # 检查 learning-checkin 是否安装
    if not check_learning_checkin():
        return {
            "require_install": True,
            "message": "需要先安装 learning-checkin 依赖"
        }
    
    # 运行 learning-checkin 打卡
    checkin_result, status = run_learning_checkin_command("checkin")
    
    # 更新配置中的学习类型
    if learning_type:
        config = load_json(CONFIG_FILE, {})
        config["learning_type"] = learning_type
        config["last_checkin"] = datetime.datetime.now().isoformat()
        save_json(CONFIG_FILE, config)
    
    # 获取已使用的名言
    used_quotes = get_used_quotes()
    
    # 构建返回消息
    streak_info = ""
    if checkin_result and checkin_result.get("streak"):
        streak = checkin_result.get("streak", 0)
        streak_info = f"\n当前连续打卡：{streak} 天"
    
    message = f"""恭喜！今日英语学习打卡完成！{streak_info}

学习是一个持续的过程，保持每天学习的习惯，你会看到自己的进步！

请让我为你生成今日的英语名言。我会查看之前已使用的名言，确保不重复。

明天继续加油！"""
    
    return {
        "success": True,
        "message": message,
        "streak": checkin_result.get("streak") if checkin_result else 0,
        "used_quotes": used_quotes,
        "learning_checkin_result": checkin_result
    }


def handle_status():
    """处理状态查询"""
    # 检查 learning-checkin 是否安装
    if not check_learning_checkin():
        return {
            "require_install": True,
            "message": "需要先安装 learning-checkin 依赖"
        }
    
    # 运行 learning-checkin 状态查询
    status_result, status = run_learning_checkin_command("status")
    
    # 获取配置
    config = load_json(CONFIG_FILE, {})
    learning_type = config.get("learning_type", "未设置")
    
    # 获取已使用的名言数量
    used_quotes = get_used_quotes()
    
    return {
        "learning_type": learning_type,
        "status": status_result,
        "used_quotes_count": len(used_quotes)
    }


def handle_get_used_quotes():
    """获取已使用的名言列表"""
    used_quotes = get_used_quotes()
    return {
        "used_quotes": used_quotes,
        "count": len(used_quotes)
    }


def handle_record_quote(quote_text):
    """记录已使用的名言"""
    ensure_data_dir()
    used_quotes = get_used_quotes()
    # 使用名言文本的哈希作为标识
    quote_hash = hash(quote_text)
    if quote_hash not in used_quotes:
        used_quotes.append(quote_hash)
        save_used_quotes(used_quotes)
    return {
        "success": True,
        "quote_recorded": quote_text[:50] + "..." if len(quote_text) > 50 else quote_text,
        "total_used": len(used_quotes)
    }


def handle_set_learning_type(learning_type):
    """设置学习类型"""
    ensure_data_dir()
    config = load_json(CONFIG_FILE, {})
    config["learning_type"] = learning_type
    save_json(CONFIG_FILE, config)
    return {
        "success": True,
        "message": f"学习类型已设置为：{learning_type}"
    }


def main():
    """主函数"""
    # 先解析全局参数
    parse_global_args()
    
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "缺少命令参数",
            "usage": "python english_checkin.py <command> [args...]"
        }, ensure_ascii=False))
        return
    
    command = sys.argv[1]
    
    try:
        if command == "init":
            result = handle_init()
            print(json.dumps(result, ensure_ascii=False))
            
        elif command == "checkin":
            learning_type = sys.argv[2] if len(sys.argv) > 2 else None
            result = handle_checkin(learning_type)
            print(json.dumps(result, ensure_ascii=False))
            
        elif command == "status":
            result = handle_status()
            print(json.dumps(result, ensure_ascii=False))
            
        elif command == "used-quotes":
            result = handle_get_used_quotes()
            print(json.dumps(result, ensure_ascii=False))
            
        elif command == "record-quote":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "请指定名言内容"}, ensure_ascii=False))
                return
            quote_text = sys.argv[2]
            result = handle_record_quote(quote_text)
            print(json.dumps(result, ensure_ascii=False))
            
        elif command == "set-type":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "请指定学习类型"}, ensure_ascii=False))
                return
            learning_type = sys.argv[2]
            result = handle_set_learning_type(learning_type)
            print(json.dumps(result, ensure_ascii=False))
            
        elif command == "version":
            print(json.dumps({"version": SKILL_VERSION}, ensure_ascii=False))
            
        elif command == "check":
            if check_learning_checkin():
                result = run_learning_checkin_command("version")
                print(json.dumps({
                    "learning_checkin_installed": True,
                    "learning_checkin_version": result[0].get("version") if result[0] else "unknown"
                }, ensure_ascii=False))
            else:
                print(json.dumps({
                    "learning_checkin_installed": False,
                    "hint": "请使用 --learning-checkin-path 参数指定 learning_checkin.py 的路径"
                }, ensure_ascii=False))
                
        else:
            print(json.dumps({
                "error": f"未知命令: {command}",
                "available_commands": ["init", "checkin", "status", "used-quotes", "record-quote", "set-type", "version", "check"]
            }, ensure_ascii=False))
            
    except Exception as e:
        print(json.dumps({
            "error": str(e)
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()