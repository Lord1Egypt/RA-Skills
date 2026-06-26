---
name: drive-tools

description: Drive Tools (云盘工具). 
  A cloud drive CLI tool supporting SMB, WebDAV, and FTP protocols, providing file listing, uploading, downloading, and remote management functions to expand storage access boundaries. 
  (支持 SMB、WebDAV 和 FTP 协议的云盘命令行工具，提供文件列表查看、上传、下载及远程管理功能，扩展存储访问边界。)
---

# drive-tools

This `drive-tools` skill helps you connect and manage your personal drives. (此 `drive-tools` 技能可协助您连接并管理个人云盘。)

## Directory Structure (目录结构)

```
drive-tools/
├── SKILL.md                    # Skill documentation (技能说明文档)
├── config.json                 # Configuration file (配置文件)
├── ftp_usage_guide.md          # FTP usage guide (FTP 使用指南)
├── smb_usage_guide.md          # SMB usage guide (SMB 使用指南)
├── webdav_usage_guide.md       # WebDAV usage guide (WebDAV 使用指南)
└── scripts/                    # Scripts directory (脚本目录)
    ├── ftp_drive_tools.py      # FTP drive tools (FTP 云盘工具)
    ├── smb_drive_tools.py      # SMB drive tools (SMB 云盘工具)
    └── webdav_drive_tools.py   # WebDAV drive tools (WebDAV 云盘工具)
```


## How to Use Drive Tools (如何使用云盘工具)

### Step 1: Understand Needs (第一步：了解需求，明确云盘类型)
Understand the user's needs and determine which type of drive needs to be accessed and managed. (明确用户的需求，确认需要访问管理的是哪种类型的云盘。)

### Step 2: Load Usage Guide (第二步：加载对应云盘类型使用指南)
According to the type of drive the user needs to access, load the usage guide for the corresponding drive type. (根据用户需要访问云盘的类型，加载对应类型云盘使用指南)

#### Usage Guide (使用指南)
- [smb](smb_usage_guide.md)
- [ftp](ftp_usage_guide.md)
- [webdav](webdav_usage_guide.md)

### Step 3: Guide Configuration of Drive Information (第三步：引导用户配置相关云盘信息)
- Use code block format strictly to guide users in filling in configuration information. (严格使用代码块格式，引导用户填写配置信息。)
- Based on the drive type, check the configuration information. If the relevant drive configuration does not exist, guide the user to configure the drive connection information and record it in `skills/drive-tools/config.json` following the specified format. Note: Do not modify existing values without user confirmation. Pay special attention to the `name` (alias) field, as it will be used to identify the drive in subsequent operations. (根据对应云盘类型，检查配置信息，如果相关云盘配置不存在需要引导用户配置云盘连接信息，并将相关配置按照相关格式追加记录到 `skills/drive-tools/config.json`。注意不要改动配置文件中原有的值，如需改变一定要提示用户进行确认。尤其要注意 `name` 别名字段，用户后续会用别名进行描述指定的云盘操作。)
- After the user enters the configuration information, perform a connection test. If the connection test fails, prompt the user to re-confirm the configuration information. If the connection test is successful, provide some suggested questions based on the drive alias set by the user. e.g., "Help me check what is in the cloud drive {name}?" (当用户输入配置信息后，进行连接测试。如果连接测试失败，则提示用户再次确认配置信息。如果连接测试成功，则根据用户设置的云盘别名内容，提示用户可以用的相关问法。例如：“帮我查看下云盘 {name} 里有些什么？”)
### Step 4: Execute Commands and Return Results (第四步：执行命令并返回结果)
Execute the corresponding commands based on user requirements and return the results. If the tool fails, notify the user immediately. (根据用户的需求，执行相应命令，并返回结果。若工具返回失败，应立即通知用户。)


## Usage Note (使用注意)

- Please ensure you confirm the whitelist path before retrieving files. Do not use the default path for downloading. It is recommended to download files to the `downloads` directory within a whitelist path that has send permissions, such as the default whitelist path for `openclaw`: `~/.openclaw/media`. Please remember this at all times. (请务必在获取文件前确认白名单路径，不要使用默认路径进行下载。建议将文件下载到有发送权限的白名单目录下的 `downloads` 目录中，例如 `openclaw` 的默认白名单路径：`~/.openclaw/media`。请务必时刻牢记。)
Example: FTP downloading `video.mp4`:
```bash
python scripts/ftp_drive_tools.py --name ftpDrive get /Movies/video.mp4 ~/.openclaw/media/downloads/video.mp4
```

- **Handling Spaces & Special Characters (处理空格和特殊字符)**: If the filename or path contains spaces or special characters (like Chinese), you **MUST** wrap the path in double quotes (`"path"`). (如果文件名或路径中包含空格或特殊字符（如中文），您**必须**使用双引号包裹路径。)
```bash
python scripts/ftp_drive_tools.py --name ftpDrive get "周杰伦 - Intro.flac" "./周杰伦 - Intro.flac"
```
