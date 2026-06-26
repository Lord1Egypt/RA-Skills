# CmdNotify

轻量级命令监控工具，用 Go 编写，资源消耗极低。

## 功能

- 批量监控多个命令/脚本
- 自定义每个命令的执行周期
- 自动检测输出变化（stdout/stderr + 退出码）
- 变化时触发告警
- 协程池 + 超时控制，内存占用极小

## 安装

```bash
go build -o cmdnotify .
```

## 使用

```bash
./cmdnotify -config config.json
```

## 配置示例

```json
{
  "commands": [
    {
      "name": "disk_usage",
      "command": "df -h /",
      "interval": "30s",
      "timeout": "10s",
      "notify_on": ["change"]
    }
  ]
}
```

## 标签

`monitoring` `alerting` `devops` `system` `go` `cli`
