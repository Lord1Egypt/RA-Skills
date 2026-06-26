package topic

import (
	"fmt"

	"github.com/spf13/cobra"
	"github.com/tencentcloud/cls-cli/internal/cmdutil"
	"github.com/tencentcloud/cls-cli/internal/output"
)

func RegisterShortcuts(rootCmd *cobra.Command, f *cmdutil.Factory) {
	topicCmd := &cobra.Command{
		Use:   "topic",
		Short: "日志主题管理",
		Long:  "日志主题和日志集的管理命令",
	}

	topicCmd.AddCommand(newListCmd(f))
	topicCmd.AddCommand(newCreateCmd(f))
	topicCmd.AddCommand(newInfoCmd(f))
	topicCmd.AddCommand(newDeleteCmd(f))
	topicCmd.AddCommand(newLogsetListCmd(f))

	rootCmd.AddCommand(topicCmd)
}

func newListCmd(f *cmdutil.Factory) *cobra.Command {
	var (
		topicName string
		logsetID  string
		offset    int64
		limit     int64
	)

	cmd := &cobra.Command{
		Use:   "+list",
		Short: "列出日志主题",
		Long: `列出当前 Region 下的日志主题。

示例:
  cls-cli topic +list
  cls-cli topic +list --name nginx
  cls-cli topic +list --logset <logset_id>
  cls-cli topic +list --format table`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if f.DryRun {
				fmt.Fprintf(f.IOStreams.Out, "DRY RUN:\n  Action: DescribeTopics\n")
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
			if topicName != "" {
				filters = append(filters, map[string]interface{}{
					"Key":    "topicName",
					"Values": []string{topicName},
				})
			}
			if logsetID != "" {
				filters = append(filters, map[string]interface{}{
					"Key":    "logsetId",
					"Values": []string{logsetID},
				})
			}
			if len(filters) > 0 {
				params["Filters"] = filters
			}

			result, err := clsClient.Call("DescribeTopics", params)
			if err != nil {
				return err
			}

			formatTopicListResult(result, f.Format)
			return nil
		},
	}

	cmd.Flags().StringVar(&topicName, "name", "", "按主题名称过滤")
	cmd.Flags().StringVar(&logsetID, "logset", "", "按日志集 ID 过滤")
	cmd.Flags().Int64Var(&offset, "offset", 0, "偏移量")
	cmd.Flags().Int64Var(&limit, "limit", 20, "返回条数")
	return cmd
}

func newCreateCmd(f *cmdutil.Factory) *cobra.Command {
	var (
		logsetID  string
		topicName string
		ttl       int64
		partCount int64
		desc      string
	)

	cmd := &cobra.Command{
		Use:   "+create",
		Short: "创建日志主题",
		Long: `创建一个新的日志主题。

示例:
  cls-cli topic +create --logset <logset_id> --name "nginx-access" --ttl 30`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if logsetID == "" || topicName == "" {
				return fmt.Errorf("--logset 和 --name 参数必填")
			}

			if f.DryRun {
				fmt.Fprintf(f.IOStreams.Out, "DRY RUN:\n  Action: CreateTopic\n  LogsetId: %s\n  TopicName: %s\n  TTL: %d\n", logsetID, topicName, ttl)
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			params := map[string]interface{}{
				"LogsetId":       logsetID,
				"TopicName":      topicName,
				"Period":         ttl,
				"PartitionCount": partCount,
			}
			if desc != "" {
				params["Describes"] = desc
			}

			result, err := clsClient.Call("CreateTopic", params)
			if err != nil {
				return err
			}

			output.FormatOutput(result, f.Format)
			output.PrintSuccess("日志主题创建成功")
			return nil
		},
	}

	cmd.Flags().StringVar(&logsetID, "logset", "", "日志集 ID（必填）")
	cmd.Flags().StringVar(&topicName, "name", "", "主题名称（必填）")
	cmd.Flags().Int64Var(&ttl, "ttl", 30, "数据保留天数")
	cmd.Flags().Int64Var(&partCount, "partitions", 1, "分区数量")
	cmd.Flags().StringVar(&desc, "desc", "", "主题描述")
	return cmd
}

func newInfoCmd(f *cmdutil.Factory) *cobra.Command {
	var topicID string

	cmd := &cobra.Command{
		Use:   "+info",
		Short: "查看日志主题详情",
		Long: `获取指定日志主题的详细信息。

示例:
  cls-cli topic +info --topic <topic_id>`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if topicID == "" {
				return fmt.Errorf("--topic 参数必填")
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			params := map[string]interface{}{
				"Filters": []map[string]interface{}{
					{"Key": "topicId", "Values": []string{topicID}},
				},
			}

			result, err := clsClient.Call("DescribeTopics", params)
			if err != nil {
				return err
			}

			output.FormatOutput(result, f.Format)
			return nil
		},
	}

	cmd.Flags().StringVar(&topicID, "topic", "", "日志主题 ID（必填）")
	return cmd
}

func newDeleteCmd(f *cmdutil.Factory) *cobra.Command {
	var topicID string

	cmd := &cobra.Command{
		Use:   "+delete",
		Short: "删除日志主题",
		Long: `删除指定的日志主题。此操作不可逆！

示例:
  cls-cli topic +delete --topic <topic_id>`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if topicID == "" {
				return fmt.Errorf("--topic 参数必填")
			}

			if f.DryRun {
				fmt.Fprintf(f.IOStreams.Out, "DRY RUN:\n  Action: DeleteTopic\n  TopicId: %s\n", topicID)
				return nil
			}

			if !f.ConfirmAction(fmt.Sprintf("即将删除日志主题 %s，此操作不可逆！", topicID)) {
				fmt.Fprintln(f.IOStreams.ErrOut, "已取消删除操作")
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			params := map[string]interface{}{
				"TopicId": topicID,
			}

			_, err = clsClient.Call("DeleteTopic", params)
			if err != nil {
				return err
			}

			output.PrintSuccess(fmt.Sprintf("日志主题 %s 已删除", topicID))
			return nil
		},
	}

	cmd.Flags().StringVar(&topicID, "topic", "", "日志主题 ID（必填）")
	return cmd
}

func newLogsetListCmd(f *cmdutil.Factory) *cobra.Command {
	var (
		logsetName string
		offset     int64
		limit      int64
	)

	cmd := &cobra.Command{
		Use:   "+logsets",
		Short: "列出日志集",
		Long: `列出当前 Region 下的日志集。

示例:
  cls-cli topic +logsets
  cls-cli topic +logsets --format table`,
		RunE: func(cmd *cobra.Command, args []string) error {
			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			params := map[string]interface{}{
				"Offset": offset,
				"Limit":  limit,
			}
			if logsetName != "" {
				params["Filters"] = []map[string]interface{}{
					{"Key": "logsetName", "Values": []string{logsetName}},
				}
			}

			result, err := clsClient.Call("DescribeLogsets", params)
			if err != nil {
				return err
			}

			output.FormatOutput(result, f.Format)
			return nil
		},
	}

	cmd.Flags().StringVar(&logsetName, "name", "", "按日志集名称过滤")
	cmd.Flags().Int64Var(&offset, "offset", 0, "偏移量")
	cmd.Flags().Int64Var(&limit, "limit", 20, "返回条数")
	return cmd
}

func formatTopicListResult(data interface{}, format output.Format) {
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
		if topics, ok := resp["Topics"].([]interface{}); ok {
			rows := make([]interface{}, 0, len(topics))
			for _, t := range topics {
				if m, ok := t.(map[string]interface{}); ok {
					rows = append(rows, map[string]interface{}{
						"TopicId":    m["TopicId"],
						"TopicName":  m["TopicName"],
						"LogsetId":   m["LogsetId"],
						"Period":     m["Period"],
						"Status":     m["Status"],
						"CreateTime": m["CreateTime"],
					})
				}
			}
			output.FormatOutput(rows, format)
			return
		}
	}
	output.FormatOutput(data, format)
}

