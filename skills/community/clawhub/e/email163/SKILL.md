# 163邮箱发送工具

基于Go开发的163邮箱SMTP发送工具。支持HTML格式、多收件人和实时日志记录。

## 编译安装

```bash
# 编译生成可执行文件
go build -o email163 main.go

# 将可执行文件移动到PATH目录（可选）
sudo mv email163 /usr/local/bin/

# 或者直接使用go install
go install
```

## 基本发送

```bash
email163 --subject "邮件标题" --info "邮件内容" --to user@example.com
email163 --subject "测试邮件" --info "这是测试内容" --to user1@example.com --to user2@example.com
email163 --subject "通知" --info "内容" --to user1@example.com,user2@example.com
```

## HTML格式邮件

```bash
email163 --subject "HTML邮件" --info "<html><body><h1>标题</h1><p>这是<b>粗体</b>内容</p></body></html>" --to user@example.com
email163 --subject "富文本通知" --info "<html><body><h2>重要通知</h2><ul><li>项目更新</li><li>系统维护</li></ul></body></html>" --to admin@example.com
```

## 带日志记录

```bash
email163 --subject "邮件标题" --info "内容" --to user@example.com --log ./logs
email163 --subject "重要通知" --info "内容" --to user@example.com --log /var/log/email
```

## 参数说明

- `--subject <标题>`: 邮件标题（必需）
- `--info <内容>`: 邮件内容，支持HTML格式（必需）
- `--to <邮箱>`: 收件人邮箱地址，可多次使用（必需）
- `--log <路径>`: 日志文件保存路径（可选，默认当前目录）
- `--help`: 显示帮助信息

## 多收件人方式

```bash
# 方式1：多次使用 --to 参数
email163 --subject "群发邮件" --info "内容" --to user1@example.com --to user2@example.com --to user3@example.com

# 方式2：逗号分隔多个邮箱
email163 --subject "群发邮件" --info "内容" --to user1@example.com,user2@example.com,user3@example.com
```

## HTML内容示例

```bash
# 简单HTML
email163 --subject "格式化邮件" --info "<html><body><p>普通文本</p><p><b>粗体文本</b></p><p><i>斜体文本</i></p></body></html>" --to user@example.com

# 复杂HTML结构
email163 --subject "详细通知" --info "<html><body><h2>系统通知</h2><p>尊敬的用户：</p><ul><li>系统将于今晚维护</li><li>预计维护时间2小时</li></ul><p>如有疑问请联系：<a href='mailto:support@example.com'>技术支持</a></p></body></html>" --to user@example.com
```

## 日志功能

- 日志文件格式：`YYYY_MM_DD_email.log`
- 记录内容：发送时间、标题、收件人、内容、结果
- 同日期自动追加，新日期创建新文件
- 自动创建日志目录

注意事项：
- 需要设置环境变量 `EMAIL163_ADDRESS` 和 `EMAIL163_PASSWORD`
- `EMAIL163_PASSWORD` 应使用163邮箱的授权码，不是登录密码
- HTML内容以 `<html>` 开头时使用用户格式，否则自动包装
- 邮箱地址会进行格式验证
- 日志内容超过200字符时会自动截断

## 环境变量设置

```bash
export EMAIL163_ADDRESS="your-email@163.com"
export EMAIL163_PASSWORD="your-authorization-code"
```

获取163邮箱授权码：
1. 登录163邮箱设置
2. 开启SMTP服务
3. 生成授权码用作密码
