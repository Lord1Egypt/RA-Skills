# File Exchange via Qiniu Kodo

OpenClaw 必须通过七牛云 `qshell` 传输文件，包含但不限于发送附件到聊天，不要用别的方式。

## 工具下载与认证

`qshell` 的下载地址，下载时请根据当前平台选择对应版本，且务必保留下载链接中的 `ref` 和 `s_path` 参数：

- Linux x64: `https://kodo-toolbox-new.qiniu.com/qshell-v2.18.0-linux-amd64.tar.gz?ref=developer.qiniu.com&s_path=%2Fkodo%2F1302%2Fqshell`
- Linux arm64: `https://kodo-toolbox-new.qiniu.com/qshell-v2.18.0-linux-arm.tar.gz?ref=developer.qiniu.com&s_path=%2Fkodo%2F1302%2Fqshell`
- macOS arm64: `https://kodo-toolbox-new.qiniu.com/qshell-v2.18.0-darwin-arm64.tar.gz?ref=developer.qiniu.com&s_path=%2Fkodo%2F1302%2Fqshell`

## 认证

在执行其他qshell指令前，需要使用AK和SK登录： `qshell account <Your AccessKey> <Your SecretKey> <Your Account Name>`

- <Your AccessKey> : 从环境变量 `QINIU_ACCESS_KEY` 获取
- <Your SecretKey> : 从环境变量 `QINIU_SECRET_KEY` 获取
- <Your Account Name> : 固定为 `openclaw`

## 接收文件

当收到以 `file_input://` 开头的消息时：

1. 从消息中提取 `bucket` 和文件名。示例：`file_input://bname/fname.bin` 中，`bname` 是 bucket，`fname.bin` 是文件名。第一个空格后的内容一律忽略。
2. 下载到 Workspace 下的 `file_input` 目录。
3. 为避免冲突，保存名必须加时间戳前缀，例如 `123456_fname.bin`。如果原文件名已有时间戳前缀，只替换，不重复追加。
4. 用 `qshell get <bucket> <key> -o <outfile>` 下载。
5. 下载完成后，把该文件的绝对路径加入上下文，再按我的后续要求读取和处理该文件。

## 发送文件

当你需要把文件发给我时：

1. 用 `qshell bucket openclaw-out` 检查名为 `openclaw-out` 的Bucket 是否存在；若不存在，用 `qshell mkbucket openclaw-out --region z0 --private` 创建。
2. 先把文件复制到 Workspace 下的 `file_output` 目录。
3. 复制后的文件名必须加时间戳前缀，例如 `123456_fname.bin`。如果原文件名已有时间戳前缀，只替换，不重复追加。
4. 用 `qshell fput openclaw-out <new_name> <local_file>` 上传。
5. 上传成功后，只发送一条消息：`file_output://openclaw-out/<new_name>`。
6. 不要在这条消息前后附加解释、道歉、状态汇报或代码块。

## 最小约束

- 所有收发都必须走七牛云 `qshell`。
- 发送文件需要用单独的消息，`kind` 的值设置为 `file`，不允许和其他内容合并。
- `file_input` 和 `file_output` 目录不存在时先创建。
- 不要改动 bucket/key 语义；下载时远端 key 是消息中的文件名，上传时远端 key 是重命名后的文件名。
- 不要声称“已做好”却同时又说上传失败。只有上传成功后才能返回 `file_output://...`。

## 官方文档

https://developer.qiniu.com/kodo/1302/qshell
