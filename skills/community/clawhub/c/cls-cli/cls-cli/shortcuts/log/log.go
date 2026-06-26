package log

import (
	"encoding/json"
	"fmt"
	"os"
	"time"

	"github.com/spf13/cobra"
	"github.com/tencentcloud/cls-cli/internal/cmdutil"
	"github.com/tencentcloud/cls-cli/internal/output"
	"github.com/tencentcloud/cls-cli/shortcuts/common"
)

func RegisterShortcuts(rootCmd *cobra.Command, f *cmdutil.Factory) {
	logCmd := &cobra.Command{
		Use:   "log",
		Short: "日志检索相关命令",
		Long:  "日志检索域：搜索、上下文查询、实时追踪、直方图统计等",
	}

	logCmd.AddCommand(newSearchCmd(f))
	logCmd.AddCommand(newContextCmd(f))
	logCmd.AddCommand(newTailCmd(f))
	logCmd.AddCommand(newHistogramCmd(f))
	logCmd.AddCommand(newDownloadCmd(f))

	rootCmd.AddCommand(logCmd)
}

func newSearchCmd(f *cmdutil.Factory) *cobra.Command {
	var (
		topicID string
		query   string
		from    string
		to      string
		limit   int64
		sort_   string
	)

	cmd := &cobra.Command{
		Use:   "+search",
		Short: "搜索日志",
		Long: `搜索指定日志主题中的日志数据。

默认搜索最近 15 分钟的日志。支持 CQL 语法和 SQL 分析。

示例:
  # 搜索 ERROR 日志
  cls-cli log +search --topic <topic_id> --query "level:ERROR"

  # 指定时间范围
  cls-cli log +search --topic <topic_id> --query "status:500" --from "2026-03-29 00:00:00" --to "2026-03-29 12:00:00"

  # 自然语言时间
  cls-cli log +search --topic <topic_id> --query "level:ERROR" --from "15 minutes ago"

  # SQL 分析
  cls-cli log +search --topic <topic_id> --query "* | SELECT status, COUNT(*) as cnt GROUP BY status ORDER BY cnt DESC LIMIT 10"

  # table 格式输出
  cls-cli log +search --topic <topic_id> --query "level:ERROR" --format table`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if topicID == "" {
				return fmt.Errorf("--topic 参数必填")
			}

			fromMs, toMs, err := resolveTimeRange(from, to)
			if err != nil {
				return err
			}

			if f.DryRun {
				fmt.Fprintf(f.IOStreams.Out, "DRY RUN:\n  Action: SearchLog\n  TopicId: %s\n  Query: %s\n  From: %d\n  To: %d\n  Limit: %d\n", topicID, query, fromMs, toMs, limit)
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			params := map[string]interface{}{
				"TopicId":    topicID,
				"Query":      query,
				"From":       fromMs,
				"To":         toMs,
				"Limit":      limit,
				"SyntaxRule": 1,
			}
			if sort_ != "" {
				params["Sort"] = sort_
			}

			result, err := clsClient.Call("SearchLog", params)
			if err != nil {
				return err
			}

			formatSearchResult(result, f.Format, f.IOStreams)
			return nil
		},
	}

	cmd.Flags().StringVar(&topicID, "topic", "", "日志主题 ID（必填）")
	cmd.Flags().StringVar(&query, "query", "*", "搜索语句（支持 CQL 和 SQL）")
	cmd.Flags().StringVar(&from, "from", "", "开始时间（默认 15 分钟前）")
	cmd.Flags().StringVar(&to, "to", "", "结束时间（默认当前）")
	cmd.Flags().Int64Var(&limit, "limit", 100, "返回条数上限")
	cmd.Flags().StringVar(&sort_, "sort", "", "排序方式: asc 或 desc")
	_ = cmd.MarkFlagRequired("topic")
	return cmd
}

func newContextCmd(f *cmdutil.Factory) *cobra.Command {
	var (
		topicID  string
		bTime    string
		pkgID    string
		pkgLogID string
		prevLogs int64
		nextLogs int64
	)

	cmd := &cobra.Command{
		Use:   "+context",
		Short: "查看日志上下文",
		Long: `根据日志定位信息查看上下文日志。

示例:
  cls-cli log +context --topic <topic_id> --btime <btime> --pkg-id <pkg_id> --pkg-log-id <pkg_log_id>`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if topicID == "" || bTime == "" || pkgID == "" || pkgLogID == "" {
				return fmt.Errorf("--topic, --btime, --pkg-id, --pkg-log-id 均为必填")
			}

			if f.DryRun {
				fmt.Fprintf(f.IOStreams.Out, "DRY RUN:\n  Action: DescribeLogContext\n  TopicId: %s\n", topicID)
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			params := map[string]interface{}{
				"TopicId":  topicID,
				"BTime":    bTime,
				"PkgId":    pkgID,
				"PkgLogId": pkgLogID,
				"PrevLogs": prevLogs,
				"NextLogs": nextLogs,
			}

			result, err := clsClient.Call("DescribeLogContext", params)
			if err != nil {
				return err
			}

			output.FormatOutput(result, f.Format)
			return nil
		},
	}

	cmd.Flags().StringVar(&topicID, "topic", "", "日志主题 ID（必填）")
	cmd.Flags().StringVar(&bTime, "btime", "", "日志时间（必填）")
	cmd.Flags().StringVar(&pkgID, "pkg-id", "", "日志包 ID（必填）")
	cmd.Flags().StringVar(&pkgLogID, "pkg-log-id", "", "日志包内序号（必填）")
	cmd.Flags().Int64Var(&prevLogs, "prev", 10, "向前查看行数")
	cmd.Flags().Int64Var(&nextLogs, "next", 10, "向后查看行数")
	return cmd
}

func newTailCmd(f *cmdutil.Factory) *cobra.Command {
	var (
		topicID  string
		query    string
		interval int
	)

	cmd := &cobra.Command{
		Use:   "+tail",
		Short: "实时追踪日志（类似 tail -f）",
		Long: `持续轮询指定主题的最新日志。

示例:
  cls-cli log +tail --topic <topic_id> --query "level:ERROR" --interval 5`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if topicID == "" {
				return fmt.Errorf("--topic 参数必填")
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			fmt.Fprintf(f.IOStreams.ErrOut, "开始追踪日志 (TopicId: %s, Query: %s, 间隔: %ds)...\n", topicID, query, interval)
			fmt.Fprintf(f.IOStreams.ErrOut, "按 Ctrl+C 停止\n\n")

			lastTo := time.Now().UnixMilli()

			for {
				fromTs := lastTo
				toTs := time.Now().UnixMilli()

				params := map[string]interface{}{
					"TopicId":    topicID,
					"Query":      query,
					"From":       fromTs,
					"To":         toTs,
					"Limit":      100,
					"SyntaxRule": 1,
					"Sort":       "asc",
				}

				result, err := clsClient.Call("SearchLog", params)
				if err != nil {
					fmt.Fprintf(f.IOStreams.ErrOut, "查询失败: %s\n", err)
				} else {
					printTailResults(result, f.IOStreams)
				}

				lastTo = toTs
				time.Sleep(time.Duration(interval) * time.Second)
			}
		},
	}

	cmd.Flags().StringVar(&topicID, "topic", "", "日志主题 ID（必填）")
	cmd.Flags().StringVar(&query, "query", "*", "过滤语句")
	cmd.Flags().IntVar(&interval, "interval", 5, "轮询间隔（秒）")
	return cmd
}

func newHistogramCmd(f *cmdutil.Factory) *cobra.Command {
	var (
		topicID  string
		query    string
		from     string
		to       string
		interval int64
	)

	cmd := &cobra.Command{
		Use:   "+histogram",
		Short: "日志数量直方图统计",
		Long: `统计指定时间范围内日志的数量分布。

示例:
  cls-cli log +histogram --topic <topic_id> --query "*" --interval 3600`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if topicID == "" {
				return fmt.Errorf("--topic 参数必填")
			}

			fromMs, toMs, err := resolveTimeRange(from, to)
			if err != nil {
				return err
			}

			if f.DryRun {
				fmt.Fprintf(f.IOStreams.Out, "DRY RUN:\n  Action: DescribeLogHistogram\n  TopicId: %s\n  Interval: %d\n", topicID, interval)
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			params := map[string]interface{}{
				"TopicId":    topicID,
				"Query":      query,
				"From":       fromMs,
				"To":         toMs,
				"SyntaxRule": 1,
			}
			if interval > 0 {
				params["Interval"] = interval
			}

			result, err := clsClient.Call("DescribeLogHistogram", params)
			if err != nil {
				return err
			}

			output.FormatOutput(result, f.Format)
			return nil
		},
	}

	cmd.Flags().StringVar(&topicID, "topic", "", "日志主题 ID（必填）")
	cmd.Flags().StringVar(&query, "query", "*", "搜索语句")
	cmd.Flags().StringVar(&from, "from", "", "开始时间（默认 1 小时前）")
	cmd.Flags().StringVar(&to, "to", "", "结束时间（默认当前）")
	cmd.Flags().Int64Var(&interval, "interval", 0, "统计间隔（毫秒，0 自动）")
	return cmd
}

func newDownloadCmd(f *cmdutil.Factory) *cobra.Command {
	var (
		topicID string
		query   string
		from    string
		to      string
		limit   int64
		outFile string
	)

	cmd := &cobra.Command{
		Use:   "+download",
		Short: "下载日志到文件",
		Long: `搜索日志并保存到本地文件。

示例:
  cls-cli log +download --topic <topic_id> --query "level:ERROR" --from "1 hour ago" -o errors.json`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if topicID == "" {
				return fmt.Errorf("--topic 参数必填")
			}
			if outFile == "" {
				return fmt.Errorf("-o 输出文件参数必填")
			}

			fromMs, toMs, err := resolveTimeRange(from, to)
			if err != nil {
				return err
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			params := map[string]interface{}{
				"TopicId":    topicID,
				"Query":      query,
				"From":       fromMs,
				"To":         toMs,
				"Limit":      limit,
				"SyntaxRule": 1,
			}

			result, err := clsClient.Call("SearchLog", params)
			if err != nil {
				return err
			}

			b, err := json.MarshalIndent(result, "", "  ")
			if err != nil {
				return err
			}

			if err := os.WriteFile(outFile, b, 0644); err != nil {
				return fmt.Errorf("写入文件失败: %w", err)
			}

			output.PrintSuccess(fmt.Sprintf("日志已保存到 %s", outFile))
			return nil
		},
	}

	cmd.Flags().StringVar(&topicID, "topic", "", "日志主题 ID（必填）")
	cmd.Flags().StringVar(&query, "query", "*", "搜索语句")
	cmd.Flags().StringVar(&from, "from", "", "开始时间（默认 1 小时前）")
	cmd.Flags().StringVar(&to, "to", "", "结束时间（默认当前）")
	cmd.Flags().Int64Var(&limit, "limit", 1000, "最大条数")
	cmd.Flags().StringVarP(&outFile, "output", "o", "", "输出文件路径（必填）")
	return cmd
}

// --- helper functions ---

func resolveTimeRange(fromStr, toStr string) (int64, int64, error) {
	var fromMs, toMs int64
	var err error

	if fromStr == "" && toStr == "" {
		fromMs, toMs = common.DefaultTimeRange(15)
		return fromMs, toMs, nil
	}

	if fromStr != "" {
		fromMs, err = common.ParseTime(fromStr)
		if err != nil {
			return 0, 0, fmt.Errorf("--from 时间解析失败: %w", err)
		}
	} else {
		fromMs, _ = common.DefaultTimeRange(60)
	}

	if toStr != "" {
		toMs, err = common.ParseTime(toStr)
		if err != nil {
			return 0, 0, fmt.Errorf("--to 时间解析失败: %w", err)
		}
	} else {
		toMs = time.Now().UnixMilli()
	}

	return fromMs, toMs, nil
}

func formatSearchResult(data interface{}, format output.Format, streams *cmdutil.IOStreams) {
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

	if analysis, ok := resp["AnalysisResults"].([]interface{}); ok && len(analysis) > 0 {
		if format == output.FormatTable || format == output.FormatCSV {
			output.FormatOutput(analysis, format)
		} else {
			output.FormatOutput(resp, format)
		}
		return
	}

	if results, ok := resp["Results"].([]interface{}); ok {
		if format == output.FormatTable || format == output.FormatCSV {
			rows := make([]interface{}, 0, len(results))
			for _, r := range results {
				if m, ok := r.(map[string]interface{}); ok {
					if logJSON, ok := m["LogJson"].(string); ok {
						var parsed map[string]interface{}
						if json.Unmarshal([]byte(logJSON), &parsed) == nil {
							rows = append(rows, parsed)
							continue
						}
					}
				}
				rows = append(rows, r)
			}
			output.FormatOutput(rows, format)
		} else {
			output.FormatOutput(resp, format)
		}
		return
	}

	output.FormatOutput(resp, format)
}

func printTailResults(data map[string]interface{}, streams *cmdutil.IOStreams) {
	resp, ok := data["Response"].(map[string]interface{})
	if !ok {
		return
	}
	results, ok := resp["Results"].([]interface{})
	if !ok || len(results) == 0 {
		return
	}
	for _, r := range results {
		if m, ok := r.(map[string]interface{}); ok {
			if logJSON, ok := m["LogJson"].(string); ok {
				fmt.Fprintln(streams.Out, logJSON)
				continue
			}
		}
		b, _ := json.Marshal(r)
		fmt.Fprintln(streams.Out, string(b))
	}
}
