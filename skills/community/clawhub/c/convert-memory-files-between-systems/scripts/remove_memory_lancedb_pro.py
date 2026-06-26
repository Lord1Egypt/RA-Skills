import json

# 读取配置文件
with open('/path/to/config.json', 'r') as file:
    config = json.load(file)

# 删除 memory-lancedb-pro 相关配置
if 'memory-lancedb-pro' in config['plugins']['entries']:
    del config['plugins']['entries']['memory-lancedb-pro']

if 'memory-lancedb-pro' in config['plugins']['load']['paths']:
    config['plugins']['load']['paths'].remove('memory-lancedb-pro')

if 'memory-lancedb-pro' in config['plugins']['allow']:
    config['plugins']['allow'].remove('memory-lancedb-pro')

# 保存配置文件
with open('/path/to/config.json', 'w') as file:
    json.dump(config, file, indent=2)