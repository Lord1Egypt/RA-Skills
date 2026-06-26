package main

import (
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/google/uuid"
)

// getDatabasePath 获取数据库文件路径
// 优先使用环境变量 TASK_SKILL_DB_PATH
// 否则使用 ~/.task-skill/tasks.db
func getDatabasePath() string {
	// 检查环境变量
	if dbPath := os.Getenv("TASK_SKILL_DB_PATH"); dbPath != "" {
		return dbPath
	}

	// 默认路径：~/.task-skill/tasks.db
	homeDir, err := os.UserHomeDir()
	if err != nil {
		// 如果无法获取主目录，回退到 /tmp/task-skill/tasks.db 避免相对路径污染当前目录
		return "/tmp/task-skill_tasks.db"
	}

	dbDir := filepath.Join(homeDir, ".task-skill")
	dbPath := filepath.Join(dbDir, "tasks.db")

	// 确保目录存在
	if err := os.MkdirAll(dbDir, 0755); err != nil {
		// 如果创建目录失败，回退到 /tmp 目录
		return "/tmp/task-skill_tasks.db"
	}

	return dbPath
}

// generateUUID 生成 UUID
func generateUUID() string {
	return uuid.New().String()
}

// getCurrentTime 获取当前时间字符串
func getCurrentTime() string {
	return time.Now().Format(time.RFC3339)
}

// formatPriority 格式化优先级显示
func formatPriority(priority int) string {
	switch priority {
	case 1:
		return "Critical"
	case 2:
		return "High"
	case 3:
		return "Medium"
	case 4:
		return "Low"
	default:
		return fmt.Sprintf("P%d", priority)
	}
}
