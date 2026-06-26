package api

import (
	"encoding/json"
	"fmt"

	"github.com/spf13/cobra"
	"github.com/tencentcloud/cls-cli/internal/cmdutil"
	"github.com/tencentcloud/cls-cli/internal/output"
)

func NewCmdApi(f *cmdutil.Factory) *cobra.Command {
	var params string

	cmd := &cobra.Command{
		Use:   "api <Action> [flags]",
		Short: "调用任意 CLS API",
		Long: `通用 API 调用，支持所有腾讯云 CLS API 3.0 接口。

示例:
  # 搜索日志
  cls-cli api SearchLog --params '{"TopicId":"xxx","Query":"level:ERROR","From":1700000000000,"To":1700003600000}'

  # 获取日志主题列表
  cls-cli api DescribeTopics --params '{"Filters":[{"Key":"topicName","Values":["nginx"]}]}'

  # 获取告警策略列表
  cls-cli api DescribeAlarms --params '{}'`,
		Args: cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			action := args[0]

			if f.DryRun {
				fmt.Fprintf(f.IOStreams.Out, "DRY RUN:\n  Action: %s\n  Params: %s\n", action, params)
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			result, err := clsClient.CallRaw(action, params)
			if err != nil {
				return err
			}

			var data interface{}
			if err := json.Unmarshal([]byte(result), &data); err != nil {
				fmt.Fprintln(f.IOStreams.Out, result)
				return nil
			}
			output.FormatOutput(data, f.Format)
			return nil
		},
	}

	cmd.Flags().StringVar(&params, "params", "{}", "请求参数 (JSON)")
	return cmd
}
