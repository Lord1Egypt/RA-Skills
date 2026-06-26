package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

var version = "0.4.3"

// Task 任务结构
type Task struct {
	ID            int64   `json:"id"`
	UUID          string  `json:"uuid"`
	Title         string  `json:"title"`
	Description   string  `json:"description,omitempty"`
	Status        string  `json:"status"`
	Priority      int     `json:"priority"`
	Project       *string `json:"project,omitempty"`
	ParentUUID    *string `json:"parent_uuid,omitempty"`
	Tags          *string `json:"tags,omitempty"`
	Assignee      *string `json:"assignee_name,omitempty"`
	AgentType     *string `json:"agent_type,omitempty"`
	AgentModel    *string `json:"agent_model,omitempty"`
	ReviewComment *string `json:"review_comment,omitempty"`
	CreatedAt     string  `json:"created_at"`
	UpdatedAt     string  `json:"updated_at"`
}

// Skill 技能结构
type Skill struct {
	tasks []Task
	db    *Database
}

// NewSkill 创建新技能实例（内存模式）
func NewSkill() *Skill {
	return &Skill{
		tasks: make([]Task, 0),
		db:    nil,
	}
}

// NewSkillWithDB 创建新技能实例（数据库模式）
func NewSkillWithDB(db *Database) *Skill {
	return &Skill{
		tasks: make([]Task, 0),
		db:    db,
	}
}

// CreateTaskInput 创建任务输入
type CreateTaskInput struct {
	Title       string   `json:"title"`
	Description string   `json:"description,omitempty"`
	Priority    int      `json:"priority,omitempty"`
	Project     string   `json:"project,omitempty"`
	ParentUUID  string   `json:"parent_uuid,omitempty"`
	Tags        []string `json:"tags,omitempty"`
	Assignee    string   `json:"assignee_name,omitempty"`
	AgentType   string   `json:"agent_type,omitempty"`
	AgentModel  string   `json:"agent_model,omitempty"`
}

// CreateTask 创建任务
func (s *Skill) CreateTask(input CreateTaskInput) map[string]interface{} {
	input.Title = strings.TrimSpace(input.Title)
	input.Project = strings.TrimSpace(input.Project)
	input.ParentUUID = strings.TrimSpace(input.ParentUUID)
	if input.Title == "" {
		return map[string]interface{}{
			"error": "标题不能为空",
		}
	}
	if input.Project == "" {
		return map[string]interface{}{
			"error": "项目不能为空",
		}
	}
	if input.Priority == 0 {
		input.Priority = 3
	}
	if input.ParentUUID != "" {
		if s.db != nil {
			parentTask, err := s.db.GetTaskByUUID(input.ParentUUID)
			if err != nil {
				return map[string]interface{}{
					"error": "父任务不存在",
				}
			}
			if parentTask.ParentUUID != nil && *parentTask.ParentUUID != "" {
				return map[string]interface{}{
					"error": "只支持2级主子任务，不能挂到子任务下",
				}
			}
		} else {
			var parentTask *Task
			for i := range s.tasks {
				if s.tasks[i].UUID == input.ParentUUID {
					parentTask = &s.tasks[i]
					break
				}
			}
			if parentTask == nil {
				return map[string]interface{}{
					"error": "父任务不存在",
				}
			}
			if parentTask.ParentUUID != nil && *parentTask.ParentUUID != "" {
				return map[string]interface{}{
					"error": "只支持2级主子任务，不能挂到子任务下",
				}
			}
		}
	}

	uuid := generateUUID()
	tagsStr := ""
	if len(input.Tags) > 0 {
		tagsStr = strings.Join(input.Tags, ",")
	}

	var project *string
	if input.Project != "" {
		project = &input.Project
	}
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
		Project:     project,
		ParentUUID:  parentUUID,
		Tags:        &tagsStr,
		Assignee:    &input.Assignee,
		AgentType:   &input.AgentType,
		AgentModel:  &input.AgentModel,
		CreatedAt:   getCurrentTime(),
		UpdatedAt:   getCurrentTime(),
	}

	// 使用数据库存储
	if s.db != nil {
		err := s.db.CreateTask(task)
		if err != nil {
			return map[string]interface{}{
				"error": fmt.Sprintf("创建任务失败：%v", err),
			}
		}
	} else {
		// 内存模式（向后兼容）
		task.ID = int64(len(s.tasks) + 1)
		s.tasks = append(s.tasks, task)
	}

	return map[string]interface{}{
		"id":      task.ID,
		"uuid":    task.UUID,
		"title":   task.Title,
		"status":  task.Status,
		"message": fmt.Sprintf("任务已创建：%s", task.Title),
	}
}

// QueryTasksInput 查询任务输入
type QueryTasksInput struct {
	Status   string `json:"status,omitempty"`
	Priority int    `json:"priority,omitempty"`
	Project  string `json:"project,omitempty"`
	Assignee string `json:"assignee_name,omitempty"`
	Keyword  string `json:"keyword,omitempty"`
	Limit    int    `json:"limit,omitempty"`
}

// QueryTasks 查询任务
func (s *Skill) QueryTasks(input QueryTasksInput) map[string]interface{} {
	var tasks []Task

	// 使用数据库查询
	if s.db != nil {
		var err error
		tasks, err = s.db.QueryTasks(input.Status, input.Priority, input.Project, input.Assignee, input.Keyword, input.Limit)
		if err != nil {
			return map[string]interface{}{
				"error": fmt.Sprintf("查询任务失败：%v", err),
			}
		}
	} else {
		// 内存模式（向后兼容）
		var filtered []Task
		for _, task := range s.tasks {
			if input.Status != "" && task.Status != input.Status {
				continue
			}
			if input.Priority != 0 && task.Priority != input.Priority {
				continue
			}
			if input.Assignee != "" && (task.Assignee == nil || *task.Assignee != input.Assignee) {
				continue
			}
			if input.Keyword != "" && !strings.Contains(task.Title, input.Keyword) {
				continue
			}
			filtered = append(filtered, task)
		}
		limit := input.Limit
		if limit == 0 || limit > len(filtered) {
			limit = len(filtered)
		}
		tasks = filtered[:limit]
	}

	return map[string]interface{}{
		"total": len(tasks),
		"tasks": tasks,
	}
}

// UpdateTaskStatusInput 更新任务状态输入
type UpdateTaskStatusInput struct {
	TaskUUID      string `json:"task_uuid"`
	NewStatus     string `json:"new_status"`
	ReviewComment string `json:"review_comment,omitempty"`
}

// UpdateTaskInput 更新任务输入
type UpdateTaskInput struct {
	TaskUUID string `json:"task_uuid"`
	Title    string `json:"title,omitempty"`
	Priority int    `json:"priority,omitempty"`
	Project  string `json:"project,omitempty"`
}

// UpdateTask 更新任务
func (s *Skill) UpdateTask(input UpdateTaskInput) map[string]interface{} {
	// 使用数据库更新
	if s.db != nil {
		err := s.db.UpdateTask(input.TaskUUID, input.Title, input.Priority, input.Project)
		if err != nil {
			return map[string]interface{}{
				"error": fmt.Sprintf("更新失败：%v", err),
			}
		}
		return map[string]interface{}{
			"uuid":    input.TaskUUID,
			"message": "任务已更新",
		}
	}

	// 内存模式（向后兼容）
	for i, task := range s.tasks {
		if task.UUID == input.TaskUUID {
			if input.Title != "" {
				s.tasks[i].Title = input.Title
			}
			if input.Priority > 0 {
				s.tasks[i].Priority = input.Priority
			}
			if input.Project != "" {
				s.tasks[i].Project = &input.Project
			}
			s.tasks[i].UpdatedAt = getCurrentTime()

			return map[string]interface{}{
				"uuid":    task.UUID,
				"message": "任务已更新",
			}
		}
	}

	return map[string]interface{}{
		"error": "任务不存在",
	}
}

// UpdateTaskStatus 更新任务状态
func (s *Skill) UpdateTaskStatus(input UpdateTaskStatusInput) map[string]interface{} {
	// 使用数据库更新
	if s.db != nil {
		err := s.db.UpdateTaskStatusWithComment(input.TaskUUID, input.NewStatus, input.ReviewComment)
		if err != nil {
			return map[string]interface{}{
				"error": fmt.Sprintf("更新失败：%v", err),
			}
		}
		return map[string]interface{}{
			"uuid":       input.TaskUUID,
			"old_status": "",
			"new_status": input.NewStatus,
			"message":    fmt.Sprintf("任务状态已更新为 %s", input.NewStatus),
		}
	}

	// 内存模式（向后兼容）
	for i, task := range s.tasks {
		if task.UUID == input.TaskUUID {
			oldStatus := task.Status
			s.tasks[i].Status = input.NewStatus
			s.tasks[i].UpdatedAt = getCurrentTime()

			return map[string]interface{}{
				"uuid":       task.UUID,
				"old_status": oldStatus,
				"new_status": input.NewStatus,
				"message":    fmt.Sprintf("任务状态已更新为 %s", input.NewStatus),
			}
		}
	}

	return map[string]interface{}{
		"error": "任务不存在",
	}
}

// ClaimTaskInput 领取任务输入
type ClaimTaskInput struct {
	TaskUUID string `json:"task_uuid"`
}

// ClaimTask 领取任务（pending → agent_working）
func (s *Skill) ClaimTask(input ClaimTaskInput) map[string]interface{} {
	return s.UpdateTaskStatus(UpdateTaskStatusInput{
		TaskUUID:  input.TaskUUID,
		NewStatus: "agent_working",
	})
}

// CompleteTaskInput 提交初审输入
type CompleteTaskInput struct {
	TaskUUID string `json:"task_uuid"`
}

// CompleteTask 提交初审（agent_working → agent_review）
func (s *Skill) CompleteTask(input CompleteTaskInput) map[string]interface{} {
	return s.UpdateTaskStatus(UpdateTaskStatusInput{
		TaskUUID:  input.TaskUUID,
		NewStatus: "agent_review",
	})
}

// ReviewTaskInput 审查任务输入
type ReviewTaskInput struct {
	TaskUUID string `json:"task_uuid"`
}

// ReviewTask 审查任务（agent_review → human_review）
func (s *Skill) ReviewTask(input ReviewTaskInput) map[string]interface{} {
	return s.UpdateTaskStatus(UpdateTaskStatusInput{
		TaskUUID:  input.TaskUUID,
		NewStatus: "human_review",
	})
}

// ApproveTaskInput 人工审核输入
type ApproveTaskInput struct {
	TaskUUID string `json:"task_uuid"`
}

// ApproveTask 人工审核通过（human_review → done）
func (s *Skill) ApproveTask(input ApproveTaskInput) map[string]interface{} {
	return s.UpdateTaskStatus(UpdateTaskStatusInput{
		TaskUUID:  input.TaskUUID,
		NewStatus: "done",
	})
}

// CancelTaskInput 取消任务输入
type CancelTaskInput struct {
	TaskUUID string `json:"task_uuid"`
}

// CancelTask 取消任务（任意状态 → cancelled）
func (s *Skill) CancelTask(input CancelTaskInput) map[string]interface{} {
	return s.UpdateTaskStatus(UpdateTaskStatusInput{
		TaskUUID:  input.TaskUUID,
		NewStatus: "cancelled",
	})
}

// RecycleTasksInput 回收任务输入
type RecycleTasksInput struct {
	DueDate string `json:"due_date"`
}

// RecycleTasks 回收到期未完成的任务（将 pending/agent_working/agent_review 状态的任务重置为 pending）
func (s *Skill) RecycleTasks(input RecycleTasksInput) map[string]interface{} {
	if s.db == nil {
		return map[string]interface{}{
			"error": "回收任务仅支持数据库模式",
		}
	}

	count, err := s.db.RecycleTasks(input.DueDate)
	if err != nil {
		return map[string]interface{}{
			"error": fmt.Sprintf("回收任务失败：%v", err),
		}
	}

	return map[string]interface{}{
		"recycled": count,
		"message":  fmt.Sprintf("已回收 %d 个到期未完成的任务", count),
	}
}

// DeleteTaskInput 删除任务输入
type DeleteTaskInput struct {
	TaskUUID string `json:"task_uuid"`
}

// DeleteTask 物理删除任务（彻底删除）
func (s *Skill) DeleteTask(input DeleteTaskInput) map[string]interface{} {
	if s.db == nil {
		return map[string]interface{}{
			"error": "删除任务仅支持数据库模式",
		}
	}

	err := s.db.DeleteTask(input.TaskUUID)
	if err != nil {
		return map[string]interface{}{
			"error": fmt.Sprintf("删除任务失败：%v", err),
		}
	}

	return map[string]interface{}{
		"uuid":    input.TaskUUID,
		"message": "任务已彻底删除",
	}
}

// GetTaskDetailInput 获取任务详情输入
type GetTaskDetailInput struct {
	TaskUUID string `json:"task_uuid"`
}

// GetTaskDetail 获取任务详情
func (s *Skill) GetTaskDetail(input GetTaskDetailInput) map[string]interface{} {
	// 使用数据库查询
	if s.db != nil {
		task, err := s.db.GetTaskByUUID(input.TaskUUID)
		if err != nil {
			return map[string]interface{}{
				"error": "任务不存在",
			}
		}
		return map[string]interface{}{
			"id":          task.ID,
			"uuid":        task.UUID,
			"title":       task.Title,
			"description": task.Description,
			"status":      task.Status,
			"priority":    task.Priority,
			"project":     task.Project,
			"parent_uuid": task.ParentUUID,
			"assignee":    task.Assignee,
			"agent_type":  task.AgentType,
			"agent_model": task.AgentModel,
			"tags":        task.Tags,
			"created_at":  task.CreatedAt,
			"updated_at":  task.UpdatedAt,
		}
	}

	// 内存模式（向后兼容）
	for _, task := range s.tasks {
		if task.UUID == input.TaskUUID {
			return map[string]interface{}{
				"id":          task.ID,
				"uuid":        task.UUID,
				"title":       task.Title,
				"description": task.Description,
				"status":      task.Status,
				"priority":    task.Priority,
				"project":     task.Project,
				"parent_uuid": task.ParentUUID,
				"assignee":    task.Assignee,
				"agent_type":  task.AgentType,
				"agent_model": task.AgentModel,
				"tags":        task.Tags,
				"created_at":  task.CreatedAt,
				"updated_at":  task.UpdatedAt,
			}
		}
	}

	return map[string]interface{}{
		"error": "任务不存在",
	}
}

// GetVersion 获取版本号
func (s *Skill) GetVersion() map[string]interface{} {
	return map[string]interface{}{
		"version": version,
	}
}

// GetDashboardStats 获取仪表盘统计
func (s *Skill) GetDashboardStats() map[string]interface{} {
	var stats map[string]int

	// 使用数据库统计
	if s.db != nil {
		var err error
		stats, err = s.db.GetDashboardStats()
		if err != nil {
			return map[string]interface{}{
				"error": fmt.Sprintf("获取统计失败：%v", err),
			}
		}
	} else {
		// 内存模式（向后兼容）
		stats = map[string]int{
			"total":         len(s.tasks),
			"pending":       0,
			"agent_working": 0,
			"agent_review":  0,
			"human_review":  0,
			"done":          0,
			"cancelled":     0,
		}
		for _, task := range s.tasks {
			switch task.Status {
			case "pending":
				stats["pending"]++
			case "agent_working":
				stats["agent_working"]++
			case "agent_review":
				stats["agent_review"]++
			case "human_review":
				stats["human_review"]++
			case "done":
				stats["done"]++
			case "cancelled":
				stats["cancelled"]++
			}
		}
	}

	return map[string]interface{}{
		"total":         stats["total"],
		"pending":       stats["pending"],
		"agent_working": stats["agent_working"],
		"agent_review":  stats["agent_review"],
		"human_review":  stats["human_review"],
		"done":          stats["done"],
		"cancelled":     stats["cancelled"],
	}
}

// RunCLI 运行 CLI 模式
func (s *Skill) RunCLI() {
	// 读取输入
	var input map[string]interface{}
	decoder := json.NewDecoder(os.Stdin)
	if err := decoder.Decode(&input); err != nil {
		fmt.Printf(`{"error": "无效的输入: %v"}`, err)
		return
	}

	// 获取函数名
	funcName, ok := input["function"].(string)
	if !ok {
		fmt.Printf(`{"error": "缺少 function 字段"}`)
		return
	}

	// 获取参数
	params := input["parameters"]

	// 调用对应的函数
	var result map[string]interface{}

	switch funcName {
	case "create_task":
		var p CreateTaskInput
		jsonBytes, _ := json.Marshal(params)
		json.Unmarshal(jsonBytes, &p)
		if p.Priority == 0 {
			p.Priority = 3 // 默认中等优先级
		}
		result = s.CreateTask(p)

	case "query_tasks":
		var p QueryTasksInput
		jsonBytes, _ := json.Marshal(params)
		json.Unmarshal(jsonBytes, &p)
		result = s.QueryTasks(p)

	case "update_task_status":
		var p UpdateTaskStatusInput
		jsonBytes, _ := json.Marshal(params)
		json.Unmarshal(jsonBytes, &p)
		result = s.UpdateTaskStatus(p)

	case "claim_task":
		var p ClaimTaskInput
		jsonBytes, _ := json.Marshal(params)
		json.Unmarshal(jsonBytes, &p)
		result = s.ClaimTask(p)

	case "submit_initial_review":
		var p CompleteTaskInput
		jsonBytes, _ := json.Marshal(params)
		json.Unmarshal(jsonBytes, &p)
		result = s.CompleteTask(p)

	case "review_task":
		var p ReviewTaskInput
		jsonBytes, _ := json.Marshal(params)
		json.Unmarshal(jsonBytes, &p)
		result = s.ReviewTask(p)

	case "approve_task":
		var p ApproveTaskInput
		jsonBytes, _ := json.Marshal(params)
		json.Unmarshal(jsonBytes, &p)
		result = s.ApproveTask(p)

	case "cancel_task":
		var p CancelTaskInput
		jsonBytes, _ := json.Marshal(params)
		json.Unmarshal(jsonBytes, &p)
		result = s.CancelTask(p)

	case "get_task_detail":
		var p GetTaskDetailInput
		jsonBytes, _ := json.Marshal(params)
		json.Unmarshal(jsonBytes, &p)
		result = s.GetTaskDetail(p)

	case "get_version":
		result = s.GetVersion()

	case "get_dashboard_stats":
		result = s.GetDashboardStats()

	case "recycle_tasks":
		var p RecycleTasksInput
		jsonBytes, _ := json.Marshal(params)
		json.Unmarshal(jsonBytes, &p)
		result = s.RecycleTasks(p)

	case "delete_task":
		var p DeleteTaskInput
		jsonBytes, _ := json.Marshal(params)
		json.Unmarshal(jsonBytes, &p)
		result = s.DeleteTask(p)

	default:
		result = map[string]interface{}{
			"error": fmt.Sprintf("未知的函数：%s", funcName),
		}
	}

	// 输出结果
	output, _ := json.MarshalIndent(result, "", "  ")
	fmt.Println(string(output))
}

func main() {
	// 检查命令行参数
	if len(os.Args) < 2 {
		printUsage()
		return
	}

	// 初始化数据库
	db, err := NewDatabase(getDatabasePath())
	if err != nil {
		fmt.Printf(`{"error": "数据库连接失败：%v"}`, err)
		return
	}
	skill := NewSkillWithDB(db)

	command := os.Args[1]

	switch command {
	case "--server", "server":
		// 启动 Web 服务器
		startServer()
	case "--version", "-v", "version":
		// 显示版本号
		fmt.Printf("task-skill version %s\n", version)
	case "--help", "-h", "help":
		printUsage()

	// 任务管理命令
	case "create-task":
		handleCreateTask(skill, os.Args[2:])
	case "list-tasks", "ls":
		handleListTasks(skill, os.Args[2:])
	case "get-task":
		handleGetTask(skill, os.Args[2:])
	case "claim-task":
		handleClaimTask(skill, os.Args[2:])
	case "submit-review":
		handleSubmitReview(skill, os.Args[2:])
	case "review-task":
		handleReviewTask(skill, os.Args[2:])
	case "approve-task":
		handleApproveTask(skill, os.Args[2:])
	case "cancel-task":
		handleCancelTask(skill, os.Args[2:])
	case "delete-task":
		handleDeleteTask(skill, os.Args[2:])
	case "recycle-tasks":
		handleRecycleTasks(skill, os.Args[2:])
	case "stats":
		handleStats(skill)

	default:
		// 兼容旧版 JSON 输入模式
		skill.RunCLI()
	}
}

func printUsage() {
	fmt.Println(`task-skill - 任务管理技能

用法: task-skill <命令> [选项]

全局命令:
  server, --server          启动 Web 服务器
  version, --version, -v    显示版本号
  help, --help, -h          显示帮助信息

任务管理命令:
  create-task               创建新任务
    --title <标题>          任务标题 (必需)
    --project <项目>        项目名称 (必需)
    --description <描述>    任务描述
    --priority <1-4>        优先级 (1=Critical, 2=High, 3=Medium, 4=Low)
    --assignee <负责人>     负责人姓名
    --parent <uuid>         父任务UUID (创建子任务)

  list-tasks, ls            列出任务
    --status <状态>         按状态筛选
    --project <项目>        按项目筛选
    --limit <数量>          限制返回数量

  get-task <uuid>           获取任务详情

  claim-task <uuid>         领取任务

  submit-review <uuid>      提交初审

  review-task <uuid>        提交人工审核

  approve-task <uuid>       人工审核通过

  cancel-task <uuid>        取消任务

  delete-task <uuid>        物理删除任务 (彻底删除，不可恢复)

  recycle-tasks             回收到期未完成任务
    --due-date <日期>       截止日期 (格式: 2026-03-22)

  stats                     显示统计信息

示例:
  task-skill create-task --title "审查文档" --project "demo" --priority 2
  task-skill list-tasks --status pending
  task-skill get-task abc-123
  task-skill claim-task abc-123
  task-skill stats`)
}

func handleCreateTask(skill *Skill, args []string) {
	input := CreateTaskInput{Priority: 3}
	for i := 0; i < len(args); i++ {
		switch args[i] {
		case "--title":
			if i+1 < len(args) {
				input.Title = args[i+1]
				i++
			}
		case "--project":
			if i+1 < len(args) {
				input.Project = args[i+1]
				i++
			}
		case "--description":
			if i+1 < len(args) {
				input.Description = args[i+1]
				i++
			}
		case "--priority":
			if i+1 < len(args) {
				fmt.Sscanf(args[i+1], "%d", &input.Priority)
				i++
			}
		case "--assignee":
			if i+1 < len(args) {
				input.Assignee = args[i+1]
				i++
			}
		case "--parent":
			if i+1 < len(args) {
				input.ParentUUID = args[i+1]
				i++
			}
		}
	}
	result := skill.CreateTask(input)
	printResult(result)
}

func handleListTasks(skill *Skill, args []string) {
	input := QueryTasksInput{}
	for i := 0; i < len(args); i++ {
		switch args[i] {
		case "--status":
			if i+1 < len(args) {
				input.Status = args[i+1]
				i++
			}
		case "--project":
			if i+1 < len(args) {
				input.Project = args[i+1]
				i++
			}
		case "--limit":
			if i+1 < len(args) {
				fmt.Sscanf(args[i+1], "%d", &input.Limit)
				i++
			}
		}
	}
	result := skill.QueryTasks(input)
	printResult(result)
}

func handleGetTask(skill *Skill, args []string) {
	if len(args) < 1 {
		fmt.Println(`{"error": "缺少任务 UUID，用法: task-skill get-task <uuid>"}`)
		return
	}
	result := skill.GetTaskDetail(GetTaskDetailInput{TaskUUID: args[0]})
	printResult(result)
}

func handleClaimTask(skill *Skill, args []string) {
	if len(args) < 1 {
		fmt.Println(`{"error": "缺少任务 UUID，用法: task-skill claim-task <uuid>"}`)
		return
	}
	result := skill.ClaimTask(ClaimTaskInput{TaskUUID: args[0]})
	printResult(result)
}

func handleSubmitReview(skill *Skill, args []string) {
	if len(args) < 1 {
		fmt.Println(`{"error": "缺少任务 UUID，用法: task-skill submit-review <uuid>"}`)
		return
	}
	result := skill.CompleteTask(CompleteTaskInput{TaskUUID: args[0]})
	printResult(result)
}

func handleReviewTask(skill *Skill, args []string) {
	if len(args) < 1 {
		fmt.Println(`{"error": "缺少任务 UUID，用法: task-skill review-task <uuid>"}`)
		return
	}
	result := skill.ReviewTask(ReviewTaskInput{TaskUUID: args[0]})
	printResult(result)
}

func handleApproveTask(skill *Skill, args []string) {
	if len(args) < 1 {
		fmt.Println(`{"error": "缺少任务 UUID，用法: task-skill approve-task <uuid>"}`)
		return
	}
	result := skill.ApproveTask(ApproveTaskInput{TaskUUID: args[0]})
	printResult(result)
}

func handleCancelTask(skill *Skill, args []string) {
	if len(args) < 1 {
		fmt.Println(`{"error": "缺少任务 UUID，用法: task-skill cancel-task <uuid>"}`)
		return
	}
	result := skill.CancelTask(CancelTaskInput{TaskUUID: args[0]})
	printResult(result)
}

func handleDeleteTask(skill *Skill, args []string) {
	if len(args) < 1 {
		fmt.Println(`{"error": "缺少任务 UUID，用法: task-skill delete-task <uuid>"}`)
		return
	}
	result := skill.DeleteTask(DeleteTaskInput{TaskUUID: args[0]})
	printResult(result)
}

func handleRecycleTasks(skill *Skill, args []string) {
	input := RecycleTasksInput{}
	for i := 0; i < len(args); i++ {
		if args[i] == "--due-date" && i+1 < len(args) {
			input.DueDate = args[i+1]
			i++
		}
	}
	result := skill.RecycleTasks(input)
	printResult(result)
}

func handleStats(skill *Skill) {
	result := skill.GetDashboardStats()
	printResult(result)
}

func printResult(result map[string]interface{}) {
	output, _ := json.MarshalIndent(result, "", "  ")
	fmt.Println(string(output))
}

// startServer 启动 Web 服务器
func startServer() {
	initServer()
}
