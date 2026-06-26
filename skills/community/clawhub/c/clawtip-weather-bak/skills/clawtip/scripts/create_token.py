import sys
from pathlib import Path
import json
import time
def create_and_save_token(token: str):
    """
    创建令牌并保存到config.json

    Args:
        token (str): 用户令牌

    Returns:
        str: 生成的令牌，如果失败则返回None
    """
    current_dir = Path(__file__).parent.absolute()
    parent_dir = current_dir.parent
    config_dir = parent_dir / 'configs'
    config_file = config_dir / 'config.json'

    # 确保configs目录存在
    try:
        config_dir.mkdir(parents=True, exist_ok=True)
        print(f"确保目录存在: {config_dir}")
    except Exception as e:
        print(f"创建目录失败: {e}")
        return None

    # 读取或创建config.json
    config_data = {}
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            print(f"已读取现有配置文件")
        except Exception as e:
            print(f"读取配置文件出错: {e}，将创建新文件")
            config_data = {}

    # 添加或更新u
    config_data['u'] = token
    timestamp = str(int(time.time()))
    config_data['lastUpdateTime'] = timestamp

    # 写入config.json
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False)
        print(f"成功将u写入配置文件")
        return token
    except Exception as e:
        print(f"写入配置文件失败: {e}")
        return None

if __name__ == "__main__":
    # 检查传入参数的数量是否正确 (1个脚本名 + 1个参数 = 2)
    if len(sys.argv) != 2:
        print("用法: create_token.py <token>")
        sys.exit(1)

    # 获取参数
    token = sys.argv[1]

    token = create_and_save_token(token)