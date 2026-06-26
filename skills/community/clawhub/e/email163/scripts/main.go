package main

// 163 邮箱发送邮件
import (
	"crypto/tls"
	"flag"
	"fmt"
	"net/smtp"
	"os"
	"path/filepath"
	"strings"
	"time"
)

var (
	smtp163Host string = "smtp.163.com"
	smtp163Port string = "465"
)

// EmailList 用于支持 --to 参数多次输入
type EmailList []string

func (e *EmailList) String() string {
	return strings.Join(*e, ", ")
}

func (e *EmailList) Set(value string) error {
	// 支持逗号分隔的多个邮箱地址
	addresses := strings.Split(value, ",")
	for _, addr := range addresses {
		addr = strings.TrimSpace(addr)
		if addr != "" {
			*e = append(*e, addr)
		}
	}
	return nil
}

// printHelp 打印帮助信息
func printHelp() {
	fmt.Printf(`163邮箱发送程序

使用方法:
  %s --subject <邮件标题> --info <邮件内容> --to <邮箱地址> [--log <日志路径>]

参数说明:
  --subject <标题>     必需，邮件标题
  --info <内容>        必需，邮件内容（支持HTML格式）
                      - 普通文本：程序会自动添加HTML标签
                      - HTML格式：如果内容以<html>开头，程序将使用您提供的HTML格式
  --to <邮箱地址>      必需，收件人邮箱地址，可以多次使用或用逗号分隔
  --log <日志路径>    	日志文件保存路径，会自动按日期创建日志文件,默认当前目录
  --help              显示此帮助信息

示例:
  # 发送普通文本邮件
  %s --subject "测试邮件" --info "这是普通文本内容" --to user1@example.com --to user2@example.com
  
  # 发送HTML格式邮件并记录日志
  %s --subject "HTML测试邮件" --info "<html><body><h1>标题</h1><p>这是<b>粗体</b>内容</p><br><a href='https://example.com'>链接</a></body></html>" --to user@example.com --log /path/to/logs
  
  # 多个收件人（逗号分隔）
  %s --subject "测试邮件" --info "这是测试内容" --to user1@example.com,user2@example.com --log ./logs

HTML内容示例:
  --info "<html><body><h2>重要通知</h2><p>尊敬的用户：</p><ul><li>项目进度更新</li><li>系统维护通知</li></ul><p>如有疑问请联系管理员。</p></body></html>"

日志功能:
  - 日志文件格式: YYYY_MM_DD_email.log
  - 记录内容: 发送时间、标题、接收方、内容、发送结果
  - 同一日期追加记录，新日期创建新文件

环境变量:
  需要设置以下环境变量：
  EMAIL163_ADDRESS   - 发送方163邮箱地址
  EMAIL163_PASSWORD  - 发送方163邮箱密码（授权码）

`, os.Args[0], os.Args[0], os.Args[0], os.Args[0])
}

// writeLog 写入日志
func writeLog(logPath, subject, content string, recipients []string, success bool, err error) {
	if logPath == "" {
		return
	}

	// 获取当前时间
	now := time.Now()
	timestamp := now.Format("2006-01-02 15:04:05")
	dateStr := now.Format("2006_01_02")

	// 构建日志文件路径
	logFileName := fmt.Sprintf("%s_email.log", dateStr)
	logFilePath := filepath.Join(logPath, logFileName)

	// 确保日志目录存在
	if err := os.MkdirAll(logPath, 0755); err != nil {
		fmt.Printf("警告: 创建日志目录失败: %v\n", err)
		return
	}

	// 构建日志内容
	result := "成功"
	if !success {
		result = fmt.Sprintf("失败: %v", err)
	}

	// 限制内容长度用于日志显示（避免日志过长）
	logContent := content
	if len(logContent) > 200 {
		logContent = logContent[:200] + "..."
	}

	logEntry := fmt.Sprintf(`
========================================
发送时间: %s
邮件标题: %s
接收方: %s
邮件内容: %s
发送结果: %s
========================================

`, timestamp, subject, strings.Join(recipients, ", "), logContent, result)

	// 打开或创建日志文件（追加模式）
	file, err := os.OpenFile(logFilePath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err != nil {
		fmt.Printf("警告: 打开日志文件失败: %v\n", err)
		return
	}
	defer file.Close()

	// 写入日志
	if _, err := file.WriteString(logEntry); err != nil {
		fmt.Printf("警告: 写入日志失败: %v\n", err)
		return
	}
}

func Get163EmailInfo(one string, permission_str string, company string, dog_id string, comment string) (string, string, error) {
	// subject := "Subject: SDK许可申请通知"
	subject := "Subject: SDK Permit Application Notice\r\n"
	info := fmt.Sprintf(`<html><body>您好:<br>

	%s 申请了权限更新。更新权限内容如下:<br><br>
	%s
<br>
	交付客户为: %s<br>
	备注信息: %s<br>
	子锁ID为: %s<br>
	如有任何疑问，请与操作员工联系．<br>
谢谢！<html><body>`, one, permission_str, company, comment, dog_id)

	return subject, info, nil
}

func Send163Email(from string, passwd string, to []string, subject string, info string) error {

	smtpHost := smtp163Host // "smtp.163.com"
	smtpPort := smtp163Port //"465"

	mime := "MIME-version: 1.0;\r\nContent-Type: text/html; charset=\"UTF-8\";\r\n\r\n"
	message := []byte(subject + mime + info)
	// 身份验证
	auth := smtp.PlainAuth("", from, passwd, smtpHost)

	// TLS配置
	tlsConfig := &tls.Config{
		InsecureSkipVerify: true,
		ServerName:         smtpHost,
	}

	// 创建TLS连接
	conn, err := tls.Dial("tcp", smtpHost+":"+smtpPort, tlsConfig)
	if err != nil {
		fmt.Println("TLS连接错误:", err)
		return err
	}

	// 创建SMTP客户端
	client, err := smtp.NewClient(conn, smtpHost)
	if err != nil {
		fmt.Println("SMTP客户端创建错误:", err)
		return err
	}
	defer client.Close()

	// 进行身份验证
	if err = client.Auth(auth); err != nil {
		fmt.Println("身份验证错误:", err)
		return err
	}

	// 设置发件人
	if err = client.Mail(from); err != nil {
		fmt.Println("设置发件人错误:", err)
		return err
	}
	// fmt.Println("toC: ", to)
	// 设置收件人
	for _, recipient := range to {
		if err = client.Rcpt(recipient); err != nil {
			fmt.Println("设置收件人错误:", err)
			return err
		}
	}

	// 发送邮件内容
	w, err := client.Data()
	if err != nil {
		fmt.Println("创建数据写入器错误:", err)
		return err
	}

	_, err = w.Write(message)
	if err != nil {
		fmt.Println("写入邮件内容错误:", err)
		return err
	}

	err = w.Close()
	if err != nil {
		fmt.Println("关闭数据写入器错误:", err)
		return err
	}
	return nil
}
func isValidEmail(email string) bool {
	// 简单的邮箱地址验证，可以根据需要进行更复杂的验证
	if len(email) < 3 || len(email) > 254 {
		return false
	}
	// 是否存在 '@' 和 '.' 字符
	atIndex := -1
	dotIndex := -1
	for i, char := range email {
		if char == '@' {
			atIndex = i
		} else if char == '.' {
			dotIndex = i
		}
	}
	return atIndex > 0 && dotIndex > atIndex+1 && dotIndex < len(email)-1
}

// 标题内容转化
func convertToEmailFormat(subject string, info string) (string, string) {
	// 转化标题
	emailSubject := "Subject: " + subject + "\r\n"

	// 先去除info前后的空白字符
	info = strings.TrimSpace(info)

	// 判断info是否以<html>开头，如果不是，则添加<html><body>标签
	if !strings.HasPrefix(info, "<html>") {
		info = fmt.Sprintf(`<html><body>%s</body></html>`, info)
	}

	return emailSubject, info
}

func main() {
	// 定义命令行参数
	var subject = flag.String("subject", "", "邮件标题（必需）")
	var info = flag.String("info", "", "邮件内容，支持HTML格式（必需）")
	var logPath = flag.String("log", "./", "日志文件保存路径（可选）")
	var toList EmailList
	var showHelp = flag.Bool("help", false, "显示帮助信息")

	flag.Var(&toList, "to", "收件人邮箱地址，可以多次使用或用逗号分隔（必需）")

	// 自定义用法信息
	flag.Usage = func() {
		printHelp()
	}

	// 解析命令行参数
	flag.Parse()
	// 当没有参数时显示帮助信息
	if len(os.Args) == 1 {
		printHelp()
		return
	}

	// 显示帮助信息
	if *showHelp {
		printHelp()
		return
	}

	// 验证必需参数
	if *subject == "" {
		fmt.Println("错误: 缺少邮件标题参数")
		fmt.Println("使用 --help 查看详细使用说明")
		os.Exit(1)
	}

	if *info == "" {
		fmt.Println("错误: 缺少邮件内容参数")
		fmt.Println("使用 --help 查看详细使用说明")
		os.Exit(1)
	}

	if len(toList) == 0 {
		fmt.Println("错误: 缺少收件人邮箱地址参数")
		fmt.Println("使用 --help 查看详细使用说明")
		os.Exit(1)
	}

	// 获取环境变量 EMAIL163_ADDRESS 和 EMAIL163_PASSWORD
	emailAddress := os.Getenv("EMAIL163_ADDRESS")
	emailPassword := os.Getenv("EMAIL163_PASSWORD")

	if emailAddress == "" || emailPassword == "" {
		fmt.Println("错误: 请设置环境变量 EMAIL163_ADDRESS 和 EMAIL163_PASSWORD")
		fmt.Println("使用 --help 查看详细使用说明")
		os.Exit(1)
	}

	// 判断接受方是否合格地址
	for _, recipient := range toList {
		if !isValidEmail(recipient) {
			fmt.Printf("错误: 无效的邮箱地址: %s\n", recipient)
			os.Exit(1)
		}
	}

	// 将标题和内容进行转化
	emailSubject, emailInfo := convertToEmailFormat(*subject, *info)

	// 发送邮件并记录日志
	err := Send163Email(emailAddress, emailPassword, toList, emailSubject, emailInfo)

	// 记录日志（无论成功与否都记录）
	writeLog(*logPath, *subject, *info, toList, err == nil, err)

	if err != nil {
		fmt.Println("发送邮件失败:", err)
		os.Exit(1)
	} else {
		fmt.Println("邮件发送成功")
	}
}
