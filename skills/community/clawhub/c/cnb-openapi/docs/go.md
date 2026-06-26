### 安装

```bash
go get cnb.cool/cnb/sdk/cnb-openapi-skills@latest
```

### API 一览

| 函数 | 说明 |
|------|------|
| `GetAPIEndpoint() string` | 从环境变量 `CNB_API_ENDPOINT` 获取 API 基础地址，默认 `https://api.cnb.cool` |
| `GetSkill() string` | 获取完整 SKILL.md 内容 |
| `GetCompactIndex() string` | 获取精简 API 索引（大幅减少 token 消耗） |
| `ListServices() ([]string, error)` | 列出所有 API 服务分类 |
| `ListAPIs(service) ([]string, error)` | 列出指定服务下的所有 API |
| `GetAPIDoc(service, api) (string, error)` | 获取指定 API 的详细文档，也支持 `GetAPIDoc("service/apiname")` 单参数调用 |
| `BuildSystemPrompt() string` | 构建 Agent 模式的 System Prompt（含精简索引 + 工作流指令） |
| `ParseAction(content) *Action` | 解析 AI 响应中的动作指令（`get_api_doc` 或 `curl`），返回 nil 表示最终回答 |
| `ExecCurl(cmd, vars, opts) CurlResult` | 执行 curl 命令，支持占位符替换和超时控制 |

### 基础用法：查询 API 文档

```go
package main

import (
	"fmt"

	skills "cnb.cool/cnb/sdk/cnb-openapi-skills"
)

func main() {
	// 列出所有服务分类
	services, _ := skills.ListServices()
	fmt.Println(services)
	// => [activities ai assets badge build git issues pulls ...]

	// 列出某个服务下的所有 API
	apis, _ := skills.ListAPIs("issues")
	fmt.Println(apis)
	// => [createissue getissue listissues updateissue ...]

	// 获取 API 详细文档（两种等价写法）
	doc, _ := skills.GetAPIDoc("issues", "createissue")
	fmt.Println(doc)

	doc, _ = skills.GetAPIDoc("issues/createissue")
	fmt.Println(doc)
}
```

### Agent 用法：结合大模型自动调用 CNB API

核心思路：用 `BuildSystemPrompt()` 构建系统提示，AI 会输出 `get_api_doc` 或 `bash` 代码块，用 `ParseAction()` 解析后执行，循环直到 AI 给出最终回答。

```go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"

	skills "cnb.cool/cnb/sdk/cnb-openapi-skills"
)

var (
	cnbToken = os.Getenv("CNB_TOKEN")
	repo     = "your-org/your-repo" // 需要有访问权限的仓库（用于调用 CNB AI 接口）
	baseURL  = skills.GetAPIEndpoint()
	maxTurns = 10
	curlVars = map[string]string{"<CNB_TOKEN>": cnbToken}
)

type message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

// 调用 CNB 平台自带 AI 接口（也可替换为 OpenAI 等兼容接口）
func chatWithCNBAI(messages []message) (string, error) {
	body, _ := json.Marshal(map[string]any{
		"model": "deepseek-chat", "stream": false, "messages": messages,
	})
	req, _ := http.NewRequest("POST",
		fmt.Sprintf("%s/%s/-/ai/chat/completions", baseURL, repo),
		bytes.NewReader(body))
	req.Header.Set("Accept", "application/vnd.cnb.api+json")
	req.Header.Set("Authorization", "Bearer "+cnbToken)
	req.Header.Set("Content-Type", "application/json")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	respBody, _ := io.ReadAll(resp.Body)

	var result struct {
		Choices []struct {
			Message struct{ Content string } `json:"message"`
		} `json:"choices"`
	}
	json.Unmarshal(respBody, &result)
	return result.Choices[0].Message.Content, nil
}

// Agent 主循环
func runAgent(userMessage string) (string, error) {
	messages := []message{
		{Role: "system", Content: skills.BuildSystemPrompt()},
		{Role: "user", Content: userMessage},
	}

	for turn := 0; turn < maxTurns; turn++ {
		aiResponse, err := chatWithCNBAI(messages)
		if err != nil {
			return "", err
		}

		action := skills.ParseAction(aiResponse)
		// 无动作指令 → AI 已给出最终回答
		if action == nil {
			return aiResponse, nil
		}

		messages = append(messages, message{Role: "assistant", Content: aiResponse})

		switch action.Type {
		case "get_api_doc":
			// AI 请求查看 API 详细文档
			doc, docErr := skills.GetAPIDoc(action.Value)
			if docErr != nil {
				doc = "错误：" + docErr.Error()
			}
			messages = append(messages, message{
				Role:    "user",
				Content: fmt.Sprintf("以下是 %s 的详细 API 文档:\n\n%s", action.Value, doc),
			})
		case "curl":
			// AI 生成了 curl 命令，执行并返回结果
			result := skills.ExecCurl(action.Value, curlVars)
			resultJSON, _ := json.MarshalIndent(result.Data, "", "  ")
			messages = append(messages, message{
				Role:    "user",
				Content: fmt.Sprintf("curl 执行结果:\n%s", string(resultJSON)),
			})
		}
	}

	return "已达到最大调用轮次，请尝试简化请求。", nil
}

func main() {
	answer, err := runAgent("帮我查看 cnb/feedback 仓库的所有分支列表，并告诉我默认分支是什么")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
	fmt.Println(answer)
}
```

### 按需加载文档（减少 token 消耗）

```go
skills "cnb.cool/cnb/sdk/cnb-openapi-skills"

// 只加载 issues 相关的 API 文档
apis, _ := skills.ListAPIs("issues")
var parts []string
for _, api := range apis {
	doc, _ := skills.GetAPIDoc("issues", api)
	parts = append(parts, doc)
}
issueContext := strings.Join(parts, "\n---\n")

systemPrompt := "你是 CNB Issue 管理助手。以下是可用的 API 文档：\n" + issueContext
```
