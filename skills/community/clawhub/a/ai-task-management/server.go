package main

import (
	"encoding/json"
	"fmt"
	"html/template"
	"io"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/google/uuid"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

var database *Database

// ServerConfig 服务器配置
type ServerConfig struct {
	Port int
}

// initServer 初始化并启动 Web 服务器
func initServer() {
	// 获取端口配置（环境变量或默认值）
	port := 8080
	if portEnv := os.Getenv("TASK_SKILL_PORT"); portEnv != "" {
		if p, err := strconv.Atoi(portEnv); err == nil {
			port = p
		}
	}

	// 初始化数据库
	var err error
	database, err = NewDatabase(getDatabasePath())
	if err != nil {
		fmt.Printf("数据库初始化失败：%v\n", err)
		os.Exit(1)
	}
	defer database.Close()

	// 创建 Echo 实例
	e := echo.New()

	// 中间件
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	// 静态文件
	e.Static("/static", "static")

	// 模板函数
	funcMap := template.FuncMap{
		"formatDate": func(dateStr string) string {
			t, err := time.Parse(time.RFC3339, dateStr)
			if err != nil {
				return dateStr
			}
			return t.Format("2006-01-02 15:04")
		},
	}

	// 模板
	t := &Template{
		templates: template.Must(template.New("").Funcs(funcMap).ParseGlob("templates/*.html")),
	}
	e.Renderer = t

	// 路由
	e.GET("/", indexHandler)
	e.GET("/tasks", tasksHandler)
	e.GET("/tasks/:uuid", taskDetailHandler)
	e.POST("/api/tasks", createTaskAPI)
	e.GET("/api/tasks", queryTasksAPI)
	e.PUT("/api/tasks/:uuid", updateTaskAPI)
	e.PUT("/api/tasks/:uuid/status", updateTaskStatusAPI)
	e.GET("/api/stats", getStatsAPI)

	// 启动服务器
	addr := fmt.Sprintf(":%d", port)
	fmt.Printf("服务器启动在 http://localhost:%d\n", port)
	fmt.Println("提示：可通过环境变量 TASK_SKILL_PORT 配置端口")
	e.Logger.Fatal(e.Start(addr))
}

// 模板渲染器
type Template struct {
	templates *template.Template
}

func (t *Template) Render(w io.Writer, name string, data interface{}, c echo.Context) error {
	return t.templates.ExecuteTemplate(w, name, data)
}

// 页面处理器
func indexHandler(c echo.Context) error {
	return c.Render(http.StatusOK, "base.html", nil)
}

func tasksHandler(c echo.Context) error {
	return c.Render(http.StatusOK, "base.html", nil)
}

func taskDetailHandler(c echo.Context) error {
	uuid := c.Param("uuid")
	task, err := database.GetTaskByUUID(uuid)
	if err != nil {
		return c.String(http.StatusNotFound, "任务不存在")
	}
	return c.Render(http.StatusOK, "base.html", task)
}

// API 处理器
func createTaskAPI(c echo.Context) error {
	var input CreateTaskInput
	if err := c.Bind(&input); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "无效的输入",
		})
	}

	input.Title = strings.TrimSpace(input.Title)
	input.Project = strings.TrimSpace(input.Project)
	input.ParentUUID = strings.TrimSpace(input.ParentUUID)

	if input.Title == "" {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "标题不能为空",
		})
	}

	if input.Project == "" {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "项目不能为空",
		})
	}

	if input.Priority == 0 {
		input.Priority = 3
	}
	if input.ParentUUID != "" {
		parentTask, err := database.GetTaskByUUID(input.ParentUUID)
		if err != nil {
			return c.JSON(http.StatusBadRequest, map[string]string{
				"error": "父任务不存在",
			})
		}
		if parentTask.ParentUUID != nil && *parentTask.ParentUUID != "" {
			return c.JSON(http.StatusBadRequest, map[string]string{
				"error": "只支持2级主子任务，不能挂到子任务下",
			})
		}
	}

	uuid := uuid.New().String()
	tagsStr := strings.Join(input.Tags, ",")
	project := input.Project
	var parentUUID *string
	if input.ParentUUID != "" {
		parentUUID = &input.ParentUUID
	}

	task := Task{
		UUID:        uuid,
		Title:       input.Title,
		Description: input.Description,
		Status:      "pending",
		Priority:    input.Priority,
		Project:     &project,
		ParentUUID:  parentUUID,
		Tags:        &tagsStr,
		Assignee:    &input.Assignee,
		AgentType:   &input.AgentType,
		AgentModel:  &input.AgentModel,
		CreatedAt:   time.Now().Format(time.RFC3339),
		UpdatedAt:   time.Now().Format(time.RFC3339),
	}

	if err := database.CreateTask(task); err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "创建失败",
		})
	}

	return c.JSON(http.StatusOK, map[string]interface{}{
		"id":          task.ID,
		"uuid":        task.UUID,
		"title":       task.Title,
		"status":      task.Status,
		"parent_uuid": task.ParentUUID,
		"message":     "任务已创建",
	})
}

func queryTasksAPI(c echo.Context) error {
	status := c.QueryParam("status")
	priority := 0
	if p := c.QueryParam("priority"); p != "" {
		priority, _ = strconv.Atoi(p)
	}
	project := c.QueryParam("project")
	assignee := c.QueryParam("assignee")
	keyword := c.QueryParam("keyword")
	limit := 20
	if l := c.QueryParam("limit"); l != "" {
		if parsed, err := strconv.Atoi(l); err == nil && parsed > 0 {
			limit = parsed
		}
	}

	tasks, err := database.QueryTasks(status, priority, project, assignee, keyword, limit)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "查询失败",
		})
	}

	return c.JSON(http.StatusOK, map[string]interface{}{
		"total": len(tasks),
		"tasks": tasks,
	})
}

func updateTaskAPI(c echo.Context) error {
	uuid := c.Param("uuid")
	var input struct {
		Title    string `json:"title"`
		Priority int    `json:"priority"`
		Project  string `json:"project"`
	}

	if err := c.Bind(&input); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "无效的输入",
		})
	}

	if err := database.UpdateTask(uuid, input.Title, input.Priority, input.Project); err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "更新失败",
		})
	}

	return c.JSON(http.StatusOK, map[string]interface{}{
		"uuid":    uuid,
		"message": "任务已更新",
	})
}

func updateTaskStatusAPI(c echo.Context) error {
	uuid := c.Param("uuid")
	var input struct {
		NewStatus     string `json:"new_status"`
		ReviewComment string `json:"review_comment"`
	}

	if err := c.Bind(&input); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "无效的输入",
		})
	}

	var err error
	if input.ReviewComment != "" {
		err = database.UpdateTaskStatusWithComment(uuid, input.NewStatus, input.ReviewComment)
	} else {
		err = database.UpdateTaskStatus(uuid, input.NewStatus)
	}

	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "更新失败",
		})
	}

	return c.JSON(http.StatusOK, map[string]interface{}{
		"uuid":       uuid,
		"new_status": input.NewStatus,
		"message":    "状态已更新",
	})
}

func getStatsAPI(c echo.Context) error {
	stats, err := database.GetDashboardStats()
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "获取统计失败",
		})
	}

	return c.JSON(http.StatusOK, stats)
}

// 辅助函数
func contains(slice []string, item string) bool {
	for _, v := range slice {
		if v == item {
			return true
		}
	}
	return false
}

func jsonEscape(str string) string {
	data, _ := json.Marshal(str)
	return string(data)[1 : len(data)-1]
}
