package collector

import (
	"encoding/json"
	"fmt"
	"strings"

	"github.com/spf13/cobra"
	"github.com/tencentcloud/cls-cli/internal/cmdutil"
	"github.com/tencentcloud/cls-cli/internal/output"
)

func RegisterShortcuts(rootCmd *cobra.Command, f *cmdutil.Factory) {
	colCmd := &cobra.Command{
		Use:   "collector",
		Short: "采集配置管理",
		Long: `管理 LogListener 的采集配置规则。

采集配置定义了：从哪些路径采集日志、使用什么解析规则、投递到哪个日志主题。

常用流程:
  1. 先创建日志主题:  cls-cli topic +create --name my-topic --logset-id xxx
  2. 再创建采集配置:  cls-cli collector +create --name my-rule --topic-id xxx --path "/var/log/app/*.log" --group-id xxx
  3. 查看采集配置:    cls-cli collector +list`,
		Aliases: []string{"col"},
	}

	colCmd.AddCommand(newListCmd(f))
	colCmd.AddCommand(newCreateCmd(f))
	colCmd.AddCommand(newDeleteCmd(f))
	colCmd.AddCommand(newInfoCmd(f))
	colCmd.AddCommand(newGuideCmd(f))

	rootCmd.AddCommand(colCmd)
}

func newListCmd(f *cmdutil.Factory) *cobra.Command {
	var topicID string

	cmd := &cobra.Command{
		Use:   "+list",
		Short: "列出采集配置",
		Long: `列出当前账号下的采集配置。

示例:
  cls-cli collector +list
  cls-cli collector +list --topic <topic_id>`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if f.DryRun {
				fmt.Fprintln(f.IOStreams.Out, "DRY RUN:\n  Action: DescribeConfigExtras")
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			params := map[string]interface{}{}
			if topicID != "" {
				params["Filters"] = []map[string]interface{}{
					{
						"Key":    "topicId",
						"Values": []string{topicID},
					},
				}
			}

			result, err := clsClient.Call("DescribeConfigExtras", params)
			if err != nil {
				return err
			}

			formatConfigList(result, f.Format, f.IOStreams)
			return nil
		},
	}

	cmd.Flags().StringVar(&topicID, "topic", "", "按日志主题 ID 过滤")
	return cmd
}

func newCreateCmd(f *cmdutil.Factory) *cobra.Command {
	var (
		name        string
		topicID     string
		logsetID    string
		logType     string
		logPath     string
		filePattern string
		groupID     string
		parseProto  string
		separator   string
		keys        string
		regex       string
		timeKey     string
		timeFormat  string
		filterKeys  string
		filterRegex string
	)

	cmd := &cobra.Command{
		Use:   "+create",
		Short: "创建采集配置",
		Long: `创建一个新的 LogListener 采集配置。

支持的日志类型:
  - fullregex:     完全正则
  - json:          JSON 格式
  - separator:     分隔符格式（如 CSV）
  - multiline:     多行全文
  - fulltext:      单行全文

示例:
  # 采集 JSON 格式日志
  cls-cli collector +create \
    --name "app-json-logs" \
    --topic <topic_id> \
    --logset <logset_id> \
    --type json \
    --path "/var/log/app" \
    --file-pattern "*.log" \
    --group-id <group_id>

  # 采集分隔符格式日志
  cls-cli collector +create \
    --name "nginx-access" \
    --topic <topic_id> \
    --logset <logset_id> \
    --type separator \
    --path "/var/log/nginx" \
    --file-pattern "access.log*" \
    --group-id <group_id> \
    --separator " " \
    --keys "remote_addr,time,method,url,status,body_bytes"

  # 采集正则格式日志
  cls-cli collector +create \
    --name "app-regex" \
    --topic <topic_id> \
    --logset <logset_id> \
    --type fullregex \
    --path "/var/log/app" \
    --file-pattern "*.log" \
    --group-id <group_id> \
    --regex "(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s\[(\w+)\]\s(.*)" \
    --keys "time,level,message"

  # 单行全文采集
  cls-cli collector +create \
    --name "simple-logs" \
    --topic <topic_id> \
    --logset <logset_id> \
    --type fulltext \
    --path "/var/log/app" \
    --file-pattern "*.log" \
    --group-id <group_id>`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if name == "" {
				return fmt.Errorf("--name 参数必填")
			}
			if topicID == "" {
				return fmt.Errorf("--topic 参数必填")
			}
			if logPath == "" {
				return fmt.Errorf("--path 参数必填")
			}
			if groupID == "" {
				return fmt.Errorf("--group-id 参数必填")
			}

			// 如果未指定 logset，自动通过 topic 查询
			if logsetID == "" && !f.DryRun {
				clsClient, err := f.CLSClient()
				if err != nil {
					return err
				}
				topicResult, err := clsClient.Call("DescribeTopics", map[string]interface{}{
					"Filters": []map[string]interface{}{
						{"Key": "topicId", "Values": []string{topicID}},
					},
				})
				if err == nil {
					if resp, ok := topicResult["Response"].(map[string]interface{}); ok {
						if topics, ok := resp["Topics"].([]interface{}); ok && len(topics) > 0 {
							if t, ok := topics[0].(map[string]interface{}); ok {
								if lid, ok := t["LogsetId"].(string); ok {
									logsetID = lid
								}
							}
						}
					}
				}
				if logsetID == "" {
					return fmt.Errorf("无法自动获取 LogsetId，请通过 --logset 参数手动指定")
				}
			}

			// 构建 HostFile 采集路径
			hostFile := map[string]interface{}{
				"LogPath":     logPath,
				"FilePattern": filePattern,
			}

			// 构建 CollectInfos
			collectInfo := map[string]interface{}{
				"Type": "host_file",
				"HostFile": hostFile,
			}

			// 构建提取规则
			extractRule := map[string]interface{}{}

			switch logType {
			case "json":
				if timeKey != "" {
					extractRule["TimeKey"] = timeKey
				}
				if timeFormat != "" {
					extractRule["TimeFormat"] = timeFormat
				}
			case "separator":
				if separator != "" {
					extractRule["Delimiter"] = separator
				}
				if keys != "" {
					extractRule["Keys"] = strings.Split(keys, ",")
				}
				if timeKey != "" {
					extractRule["TimeKey"] = timeKey
				}
				if timeFormat != "" {
					extractRule["TimeFormat"] = timeFormat
				}
			case "fullregex":
				if regex != "" {
					extractRule["LogRegex"] = regex
				}
				if keys != "" {
					extractRule["Keys"] = strings.Split(keys, ",")
				}
				if timeKey != "" {
					extractRule["TimeKey"] = timeKey
				}
				if timeFormat != "" {
					extractRule["TimeFormat"] = timeFormat
				}
			case "multiline":
				if regex != "" {
					extractRule["BeginRegex"] = regex
				}
			}

			// 过滤规则
			if filterKeys != "" && filterRegex != "" {
				fKeys := strings.Split(filterKeys, ",")
				fRegex := strings.Split(filterRegex, ",")
				extractRule["FilterKeyRegex"] = buildFilterKeyRegex(fKeys, fRegex)
			}

			if parseProto != "" {
				extractRule["ParseProtocol"] = parseProto
			}

			// 构建完整请求参数，对齐 CreateConfigExtra API 规范
			params := map[string]interface{}{
				"Name":         name,
				"TopicId":      topicID,
				"LogsetId":     logsetID,
				"Type":         "host_file",
				"LogType":      logType,
				"LogFormat":    logType,
				"ConfigFlag":   "label_k8s",
				"GroupIds":     []string{groupID},
				"CollectInfos": []interface{}{collectInfo},
				"ExtractRule":  extractRule,
				"ExcludePaths": []interface{}{},
			}

			if f.DryRun {
				b, _ := json.MarshalIndent(params, "", "  ")
				fmt.Fprintf(f.IOStreams.Out, "DRY RUN:\n  Action: CreateConfigExtra\n  Params: %s\n", string(b))
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			result, err := clsClient.Call("CreateConfigExtra", params)
			if err != nil {
				return err
			}

			if resp, ok := result["Response"].(map[string]interface{}); ok {
				if configExtraID, ok := resp["ConfigExtraId"].(string); ok {
					output.PrintSuccess(fmt.Sprintf("采集配置 '%s' 创建成功（ID: %s），已绑定机器组 %s", name, configExtraID, groupID))
				}
			}

			output.FormatOutput(result, f.Format)
			return nil
		},
	}

	cmd.Flags().StringVar(&name, "name", "", "采集配置名称（必填）")
	cmd.Flags().StringVar(&topicID, "topic", "", "投递的日志主题 ID（必填）")
	cmd.Flags().StringVar(&logsetID, "logset", "", "日志集 ID（可选，不填则自动从 topic 查询）")
	cmd.Flags().StringVar(&logType, "type", "fulltext", "日志类型: fulltext, json, separator, fullregex, multiline")
	cmd.Flags().StringVar(&logPath, "path", "", "采集日志路径（必填），如 /var/log/app")
	cmd.Flags().StringVar(&filePattern, "file-pattern", "*.log", "文件名匹配模式")
	cmd.Flags().StringVar(&groupID, "group-id", "", "机器组 ID（必填）")
	cmd.Flags().StringVar(&parseProto, "parse-proto", "", "解析协议")
	cmd.Flags().StringVar(&separator, "separator", "", "分隔符（type=separator 时使用）")
	cmd.Flags().StringVar(&keys, "keys", "", "字段名列表，逗号分隔")
	cmd.Flags().StringVar(&regex, "regex", "", "正则表达式（type=fullregex/multiline 时使用）")
	cmd.Flags().StringVar(&timeKey, "time-key", "", "时间字段名")
	cmd.Flags().StringVar(&timeFormat, "time-format", "", "时间格式，如 %Y-%m-%d %H:%M:%S")
	cmd.Flags().StringVar(&filterKeys, "filter-keys", "", "过滤字段名，逗号分隔")
	cmd.Flags().StringVar(&filterRegex, "filter-regex", "", "过滤正则，逗号分隔（与 filter-keys 一一对应）")
	_ = cmd.MarkFlagRequired("name")
	_ = cmd.MarkFlagRequired("topic")
	_ = cmd.MarkFlagRequired("path")
	_ = cmd.MarkFlagRequired("group-id")
	return cmd
}

func newDeleteCmd(f *cmdutil.Factory) *cobra.Command {
	var configID string

	cmd := &cobra.Command{
		Use:   "+delete",
		Short: "删除采集配置",
		RunE: func(cmd *cobra.Command, args []string) error {
			if configID == "" {
				return fmt.Errorf("--id 参数必填")
			}

			if f.DryRun {
				fmt.Fprintf(f.IOStreams.Out, "DRY RUN:\n  Action: DeleteConfigExtra\n  ConfigExtraId: %s\n", configID)
				return nil
			}

			if !f.ConfirmAction(fmt.Sprintf("即将删除采集配置 %s，此操作不可逆！", configID)) {
				fmt.Fprintln(f.IOStreams.ErrOut, "已取消删除操作")
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			_, err = clsClient.Call("DeleteConfigExtra", map[string]interface{}{
				"ConfigExtraId": configID,
			})
			if err != nil {
				return err
			}

			output.PrintSuccess(fmt.Sprintf("采集配置 %s 已删除", configID))
			return nil
		},
	}

	cmd.Flags().StringVar(&configID, "id", "", "采集配置 ID（必填）")
	_ = cmd.MarkFlagRequired("id")
	return cmd
}

func newInfoCmd(f *cmdutil.Factory) *cobra.Command {
	var configID string

	cmd := &cobra.Command{
		Use:   "+info",
		Short: "查看采集配置详情",
		RunE: func(cmd *cobra.Command, args []string) error {
			if configID == "" {
				return fmt.Errorf("--id 参数必填")
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			result, err := clsClient.Call("DescribeConfigExtras", map[string]interface{}{
				"Filters": []map[string]interface{}{
					{
						"Key":    "configExtraId",
						"Values": []string{configID},
					},
				},
			})
			if err != nil {
				return err
			}

			output.FormatOutput(result, f.Format)
			return nil
		},
	}

	cmd.Flags().StringVar(&configID, "id", "", "采集配置 ID（必填）")
	_ = cmd.MarkFlagRequired("id")
	return cmd
}

// +guide: 交互式引导创建采集配置
func newGuideCmd(f *cmdutil.Factory) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "+guide",
		Short: "采集配置快速入门指南",
		Long:  "展示从零开始配置 LogListener 采集的完整流程",
		Run: func(cmd *cobra.Command, args []string) {
			guide := `
=== CLS LogListener 采集配置完整流程 ===

步骤 1: 安装 LogListener（在目标服务器上执行）
  $ cls-cli loglistener +install
  $ cls-cli loglistener +init --region ap-guangzhou
  $ cls-cli loglistener +start

步骤 2: 创建机器组
  $ cls-cli machinegroup +create --name my-servers --type ip --values "10.0.0.1,10.0.0.2"

步骤 3: 创建日志集和日志主题
  $ cls-cli topic +logsets                           # 查看现有日志集
  $ cls-cli topic +create --name my-app --logset-id <logset_id>

步骤 4: 创建采集配置
  # JSON 日志
  $ cls-cli collector +create \
      --name "app-logs" \
      --topic <topic_id> \
      --type json \
      --path "/var/log/app" \
      --file-pattern "*.log" \
      --group-id <group_id>

  # 单行全文
  $ cls-cli collector +create \
      --name "syslog" \
      --topic <topic_id> \
      --type fulltext \
      --path "/var/log" \
      --file-pattern "syslog*" \
      --group-id <group_id>

步骤 5: 验证
  $ cls-cli machinegroup +status --id <group_id>     # 检查机器状态
  $ cls-cli loglistener +check                        # 检查心跳
  $ cls-cli log +search --topic <topic_id>            # 搜索日志验证

=== 常见问题 ===
Q: 没有日志上报？
  1. 检查 LogListener 状态: cls-cli loglistener +status
  2. 检查机器组状态: cls-cli machinegroup +status --id <group_id>
  3. 检查采集路径是否正确
  4. 检查日志文件权限

Q: 如何配置多行日志（如 Java 堆栈）？
  $ cls-cli collector +create \
      --type multiline \
      --regex "^\d{4}-\d{2}-\d{2}" \
      ...
`
			fmt.Fprintln(f.IOStreams.Out, guide)
		},
	}
	return cmd
}

// --- helpers ---

func buildFilterKeyRegex(keys, regexes []string) []map[string]interface{} {
	result := make([]map[string]interface{}, 0)
	for i := 0; i < len(keys) && i < len(regexes); i++ {
		result = append(result, map[string]interface{}{
			"Key":   strings.TrimSpace(keys[i]),
			"Regex": strings.TrimSpace(regexes[i]),
		})
	}
	return result
}

func formatConfigList(data map[string]interface{}, format output.Format, streams *cmdutil.IOStreams) {
	resp, ok := data["Response"].(map[string]interface{})
	if !ok {
		output.FormatOutput(data, format)
		return
	}

	configs, ok := resp["Configs"].([]interface{})
	if !ok || len(configs) == 0 {
		fmt.Fprintln(streams.ErrOut, "暂无采集配置")
		return
	}

	if format == output.FormatTable || format == output.FormatCSV {
		rows := make([]map[string]interface{}, 0, len(configs))
		for _, c := range configs {
			if m, ok := c.(map[string]interface{}); ok {
				rows = append(rows, map[string]interface{}{
					"ConfigExtraId": m["ConfigExtraId"],
					"Name":          m["Name"],
					"TopicId":       m["TopicId"],
					"LogType":       m["LogType"],
					"Path":          m["LogPath"],
					"CreateTime":    m["CreateTime"],
				})
			}
		}
		output.FormatOutput(rows, format)
	} else {
		output.FormatOutput(resp, format)
	}
}
