package dashboard

import (
	"encoding/json"
	"fmt"

	"github.com/spf13/cobra"
	"github.com/tencentcloud/cls-cli/internal/cmdutil"
	"github.com/tencentcloud/cls-cli/internal/output"
)

func RegisterShortcuts(rootCmd *cobra.Command, f *cmdutil.Factory) {
	dashboardCmd := &cobra.Command{
		Use:     "dashboard",
		Aliases: []string{"dash"},
		Short:   "仪表盘管理",
		Long:    "仪表盘域：查看、创建、修改、删除仪表盘",
	}

	dashboardCmd.AddCommand(newListCmd(f))
	dashboardCmd.AddCommand(newInfoCmd(f))
	dashboardCmd.AddCommand(newCreateCmd(f))
	dashboardCmd.AddCommand(newUpdateCmd(f))
	dashboardCmd.AddCommand(newDeleteCmd(f))

	rootCmd.AddCommand(dashboardCmd)
}

// +list 列出仪表盘
func newListCmd(f *cmdutil.Factory) *cobra.Command {
	var (
		name   string
		offset int64
		limit  int64
	)

	cmd := &cobra.Command{
		Use:   "+list",
		Short: "列出仪表盘",
		Long: `列出当前 Region 下的仪表盘。

示例:
  cls-cli dashboard +list
  cls-cli dash +list --name "运维总览"
  cls-cli dash +list --format table`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if f.DryRun {
				fmt.Fprintf(f.IOStreams.Out, "DRY RUN:\n  Action: DescribeDashboards\n")
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			params := map[string]interface{}{
				"Offset": offset,
				"Limit":  limit,
			}

			var filters []map[string]interface{}
			if name != "" {
				filters = append(filters, map[string]interface{}{
					"Key":    "dashboardName",
					"Values": []string{name},
				})
			}
			if len(filters) > 0 {
				params["Filters"] = filters
			}

			result, err := clsClient.Call("DescribeDashboards", params)
			if err != nil {
				return err
			}

			formatDashboardListResult(result, f.Format)
			return nil
		},
	}

	cmd.Flags().StringVar(&name, "name", "", "按仪表盘名称过滤")
	cmd.Flags().Int64Var(&offset, "offset", 0, "偏移量")
	cmd.Flags().Int64Var(&limit, "limit", 20, "返回条数")
	return cmd
}

// +info 查看仪表盘详情
func newInfoCmd(f *cmdutil.Factory) *cobra.Command {
	var dashboardID string

	cmd := &cobra.Command{
		Use:   "+info",
		Short: "查看仪表盘详情",
		Long: `获取指定仪表盘的详细信息，包括图表配置。

示例:
  cls-cli dashboard +info --id <dashboard_id>
  cls-cli dash +info --id <dashboard_id> --format pretty`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if dashboardID == "" {
				return fmt.Errorf("--id 参数必填")
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			params := map[string]interface{}{
				"Filters": []map[string]interface{}{
					{"Key": "dashboardId", "Values": []string{dashboardID}},
				},
			}

			result, err := clsClient.Call("DescribeDashboards", params)
			if err != nil {
				return err
			}

			output.FormatOutput(result, f.Format)
			return nil
		},
	}

	cmd.Flags().StringVar(&dashboardID, "id", "", "仪表盘 ID（必填）")
	return cmd
}

// +create 创建仪表盘
func newCreateCmd(f *cmdutil.Factory) *cobra.Command {
	var (
		name     string
		data     string
		topicID  string
		tagKey   string
		tagValue string
	)

	cmd := &cobra.Command{
		Use:   "+create",
		Short: "创建仪表盘",
		Long: `创建一个新的仪表盘。

仪表盘数据(--data)为 JSON 字符串，定义图表布局和查询配置。
如果不提供 --data，将创建一个空仪表盘。

示例:
  # 创建空仪表盘
  cls-cli dashboard +create --name "运维总览"

  # 创建并关联日志主题
  cls-cli dash +create --name "Nginx 监控" --topic <topic_id>

  # 创建并指定完整配置
  cls-cli dash +create --name "自定义仪表盘" --data '{"panels":[]}'`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if name == "" {
				return fmt.Errorf("--name 参数必填")
			}

			if f.DryRun {
				fmt.Fprintf(f.IOStreams.Out, "DRY RUN:\n  Action: CreateDashboard\n  DashboardName: %s\n", name)
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			// 默认空仪表盘配置
			if data == "" {
				data = `{"panels":[]}`
			}

			params := map[string]interface{}{
				"DashboardName": name,
				"Data":          data,
			}

			if topicID != "" {
				params["TopicId"] = topicID
			}

			if tagKey != "" && tagValue != "" {
				params["Tags"] = []map[string]interface{}{
					{"Key": tagKey, "Value": tagValue},
				}
			}

			result, err := clsClient.Call("CreateDashboard", params)
			if err != nil {
				return err
			}

			output.FormatOutput(result, f.Format)
			output.PrintSuccess("仪表盘创建成功")
			return nil
		},
	}

	cmd.Flags().StringVar(&name, "name", "", "仪表盘名称（必填）")
	cmd.Flags().StringVar(&data, "data", "", "仪表盘配置 JSON")
	cmd.Flags().StringVar(&topicID, "topic", "", "关联的日志主题 ID")
	cmd.Flags().StringVar(&tagKey, "tag-key", "", "标签键")
	cmd.Flags().StringVar(&tagValue, "tag-value", "", "标签值")
	return cmd
}

// +update 修改仪表盘
func newUpdateCmd(f *cmdutil.Factory) *cobra.Command {
	var (
		dashboardID string
		name        string
		data        string
	)

	cmd := &cobra.Command{
		Use:   "+update",
		Short: "修改仪表盘",
		Long: `修改仪表盘的名称或配置。

示例:
  # 修改名称
  cls-cli dashboard +update --id <dashboard_id> --name "新名称"

  # 修改图表配置
  cls-cli dash +update --id <dashboard_id> --data '{"panels":[...]}'

  # 同时修改名称和配置
  cls-cli dash +update --id <dashboard_id> --name "新名称" --data '{"panels":[]}'`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if dashboardID == "" {
				return fmt.Errorf("--id 参数必填")
			}

			if f.DryRun {
				fmt.Fprintf(f.IOStreams.Out, "DRY RUN:\n  Action: ModifyDashboard\n  DashboardId: %s\n", dashboardID)
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			params := map[string]interface{}{
				"DashboardId": dashboardID,
			}

			if name != "" {
				params["DashboardName"] = name
			}
			if data != "" {
				params["Data"] = data
			}

			result, err := clsClient.Call("ModifyDashboard", params)
			if err != nil {
				return err
			}

			output.FormatOutput(result, f.Format)
			output.PrintSuccess(fmt.Sprintf("仪表盘 %s 已更新", dashboardID))
			return nil
		},
	}

	cmd.Flags().StringVar(&dashboardID, "id", "", "仪表盘 ID（必填）")
	cmd.Flags().StringVar(&name, "name", "", "新的仪表盘名称")
	cmd.Flags().StringVar(&data, "data", "", "新的仪表盘配置 JSON")
	return cmd
}

// +delete 删除仪表盘
func newDeleteCmd(f *cmdutil.Factory) *cobra.Command {
	var dashboardID string

	cmd := &cobra.Command{
		Use:   "+delete",
		Short: "删除仪表盘",
		Long: `删除指定的仪表盘。此操作不可逆！

示例:
  cls-cli dashboard +delete --id <dashboard_id>
  cls-cli dash +delete --id <dashboard_id> -y`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if dashboardID == "" {
				return fmt.Errorf("--id 参数必填")
			}

			if f.DryRun {
				fmt.Fprintf(f.IOStreams.Out, "DRY RUN:\n  Action: DeleteDashboard\n  DashboardId: %s\n", dashboardID)
				return nil
			}

			if !f.ConfirmAction(fmt.Sprintf("即将删除仪表盘 %s，此操作不可逆！", dashboardID)) {
				fmt.Fprintln(f.IOStreams.ErrOut, "已取消删除操作")
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			params := map[string]interface{}{
				"DashboardIds": []string{dashboardID},
			}

			_, err = clsClient.Call("DeleteDashboard", params)
			if err != nil {
				return err
			}

			output.PrintSuccess(fmt.Sprintf("仪表盘 %s 已删除", dashboardID))
			return nil
		},
	}

	cmd.Flags().StringVar(&dashboardID, "id", "", "仪表盘 ID（必填）")
	return cmd
}

func formatDashboardListResult(data interface{}, format output.Format) {
	if format == output.FormatTable || format == output.FormatCSV {
		dataMap, ok := data.(map[string]interface{})
		if !ok {
			output.FormatOutput(data, format)
			return
		}
		resp, ok := dataMap["Response"].(map[string]interface{})
		if !ok {
			output.FormatOutput(data, format)
			return
		}

		// 尝试解析 DashboardInfos
		if dashboards, ok := resp["DashboardInfos"].([]interface{}); ok {
			rows := make([]interface{}, 0, len(dashboards))
			for _, d := range dashboards {
				if m, ok := d.(map[string]interface{}); ok {
					row := map[string]interface{}{
						"DashboardId":   m["DashboardId"],
						"DashboardName": m["DashboardName"],
						"CreateTime":    m["CreateTime"],
					}
					// Data 字段可能很长，table 模式下截断显示
					if dataStr, ok := m["Data"].(string); ok {
						var parsed interface{}
						if err := json.Unmarshal([]byte(dataStr), &parsed); err == nil {
							if pm, ok := parsed.(map[string]interface{}); ok {
								if panels, ok := pm["panels"].([]interface{}); ok {
									row["PanelCount"] = len(panels)
								}
							}
						}
					}
					rows = append(rows, row)
				}
			}
			output.FormatOutput(rows, format)
			return
		}
	}
	output.FormatOutput(data, format)
}
