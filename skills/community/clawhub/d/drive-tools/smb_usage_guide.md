# SMB Usage Guide (SMB 使用指南)

Drive configuration is automatically loaded from `config.json`. (云盘配置从 `config.json` 自动加载。)

## SMB Config Template (SMB 配置模版)

```json
{
  "name": "smbDrive", // Configuration Alias (设置别名)
  "user": "user", // SMB Username (SMB 用户名)
  "password": "password", // SMB Password (SMB 密码)
  "ip": "192.168.50.1", // Server IP address (服务器 IP 地址)
  "share": "test", // Shared folder name (共享文件夹名称)
  "domain": "WORKGROUP", // SMB Domain (SMB 域名), default WORKGROUP
  "path": "/" // Initial remote path (初始远程路径)
}
```

- Assist users in completing relevant configuration information according to the template, and record it to `skills/drive-tools/config.json`. (协助用户按模板完成相关配置信息，并记录到 `skills/drive-tools/config.json`)
- The configuration template can be output as a code block for users to fill in; do not omit any fields in the code block. (将配置模版通过代码块的格式输出给用户，让用户进行填写，代码块格式里不要缺少字段。)



## Quick Start (快速开始)

**Script (脚本):** `scripts/smb_drive_tools.py`

### Global Options (通用参数)
- `--name <config_name>`: Specify the connection name or index in `config.json` (指定 `config.json` 中的连接名称或索引).

```shell
# Test Connection (测试连接是否成功)
python scripts/smb_drive_tools.py --name smbDrive test

# List Directory (列出目录内容)
python scripts/smb_drive_tools.py --name smbDrive ls /Documents

# Upload File: local_path -> remote_path (上传本地文件: 本地路径 -> 远程路径)
python scripts/smb_drive_tools.py --name smbDrive put ./data.zip /backups/data.zip

# Download File: remote_path -> local_path (下载远程文件: 远程路径 -> 本地路径)
python scripts/smb_drive_tools.py --name smbDrive get /movies/demo.mp4 ./demo.mp4

# Create Directory (创建远程目录)
python scripts/smb_drive_tools.py --name smbDrive mkdir /projects/new_folder

# Delete File or Directory (删除远程文件或目录)
# Use -d for directories (使用 -d 参数删除目录)
python scripts/smb_drive_tools.py --name smbDrive rm /old_file.txt
python scripts/smb_drive_tools.py --name smbDrive rm -d /old_folder

# Rename or Move: old_path -> new_path (重命名或移动: 旧路径 -> 新路径)
python scripts/smb_drive_tools.py --name smbDrive mv /old_name.txt /new_name.txt

# Search Recursively (递归搜索关键字)
python scripts/smb_drive_tools.py --name smbDrive find keyword --path /

```