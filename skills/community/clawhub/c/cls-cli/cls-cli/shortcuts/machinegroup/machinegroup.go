package machinegroup

import (
	"encoding/json"
	"fmt"
	"strings"

	"github.com/spf13/cobra"
	"github.com/tencentcloud/cls-cli/internal/cmdutil"
	"github.com/tencentcloud/cls-cli/internal/output"
)

func RegisterShortcuts(rootCmd *cobra.Command, f *cmdutil.Factory) {
	mgCmd := &cobra.Command{
		Use:   "machinegroup",
		Short: "机器组管理",
		Long: `机器组是 CLS 中 LogListener 采集日志的服务器分组。

机器组有两种类型：
  - IP 地址型：通过服务器内网 IP 关联
  - 机器标识型：通过 Label 标识关联

示例:
  cls-cli machinegroup +list
  cls-cli machinegroup +create --name mygroup --type ip --values "10.0.0.1,10.0.0.2"
  cls-cli machinegroup +create --name mygroup --type label --values "webserver"`,
		Aliases: []string{"mg"},
	}

	mgCmd.AddCommand(newListCmd(f))
	mgCmd.AddCommand(newCreateCmd(f))
	mgCmd.AddCommand(newDeleteCmd(f))
	mgCmd.AddCommand(newInfoCmd(f))
	mgCmd.AddCommand(newStatusCmd(f))

	rootCmd.AddCommand(mgCmd)
}

func newListCmd(f *cmdutil.Factory) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "+list",
		Short: "列出所有机器组",
		RunE: func(cmd *cobra.Command, args []string) error {
			if f.DryRun {
				fmt.Fprintln(f.IOStreams.Out, "DRY RUN:\n  Action: DescribeMachineGroups")
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			result, err := clsClient.Call("DescribeMachineGroups", map[string]interface{}{})
			if err != nil {
				return err
			}

			formatMachineGroupList(result, f.Format, f.IOStreams)
			return nil
		},
	}
	return cmd
}

func newCreateCmd(f *cmdutil.Factory) *cobra.Command {
	var (
		name     string
		mgType   string
		values   string
		autoUpdate bool
		updateTime string
	)

	cmd := &cobra.Command{
		Use:   "+create",
		Short: "创建机器组",
		Long: `创建一个新的机器组。

示例:
  # 通过 IP 创建
  cls-cli machinegroup +create --name web-servers --type ip --values "10.0.0.1,10.0.0.2,10.0.0.3"

  # 通过标识创建
  cls-cli machinegroup +create --name web-servers --type label --values "webserver"

  # 开启自动更新
  cls-cli machinegroup +create --name web-servers --type ip --values "10.0.0.1" --auto-update --update-time "02:00"`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if name == "" {
				return fmt.Errorf("--name 参数必填")
			}
			if values == "" {
				return fmt.Errorf("--values 参数必填")
			}

			var typeStr string
			switch strings.ToLower(mgType) {
			case "ip":
				typeStr = "ip"
			case "label":
				typeStr = "label"
			default:
				return fmt.Errorf("--type 必须是 ip 或 label")
			}

			valueList := strings.Split(values, ",")
			for i := range valueList {
				valueList[i] = strings.TrimSpace(valueList[i])
			}

			params := map[string]interface{}{
				"GroupName": name,
				"MachineGroupType": map[string]interface{}{
					"Type":   typeStr,
					"Values": valueList,
				},
			}

			if autoUpdate {
				params["AutoUpdate"] = true
				if updateTime != "" {
					params["UpdateStartTime"] = updateTime
				}
			}

			if f.DryRun {
				b, _ := json.MarshalIndent(params, "", "  ")
				fmt.Fprintf(f.IOStreams.Out, "DRY RUN:\n  Action: CreateMachineGroup\n  Params: %s\n", string(b))
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			result, err := clsClient.Call("CreateMachineGroup", params)
			if err != nil {
				return err
			}

			output.PrintSuccess(fmt.Sprintf("机器组 '%s' 创建成功", name))
			output.FormatOutput(result, f.Format)
			return nil
		},
	}

	cmd.Flags().StringVar(&name, "name", "", "机器组名称（必填）")
	cmd.Flags().StringVar(&mgType, "type", "ip", "类型: ip（IP地址）, label（机器标识）")
	cmd.Flags().StringVar(&values, "values", "", "IP列表或标识，逗号分隔（必填）")
	cmd.Flags().BoolVar(&autoUpdate, "auto-update", false, "是否开启 LogListener 自动更新")
	cmd.Flags().StringVar(&updateTime, "update-time", "", "自动更新时间，如 02:00")
	_ = cmd.MarkFlagRequired("name")
	_ = cmd.MarkFlagRequired("values")
	return cmd
}

func newDeleteCmd(f *cmdutil.Factory) *cobra.Command {
	var groupID string

	cmd := &cobra.Command{
		Use:   "+delete",
		Short: "删除机器组",
		Long: `删除指定的机器组。

示例:
  cls-cli machinegroup +delete --id <group_id>`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if groupID == "" {
				return fmt.Errorf("--id 参数必填")
			}

			if f.DryRun {
				fmt.Fprintf(f.IOStreams.Out, "DRY RUN:\n  Action: DeleteMachineGroup\n  GroupId: %s\n", groupID)
				return nil
			}

			if !f.ConfirmAction(fmt.Sprintf("即将删除机器组 %s，此操作不可逆！", groupID)) {
				fmt.Fprintln(f.IOStreams.ErrOut, "已取消删除操作")
				return nil
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			_, err = clsClient.Call("DeleteMachineGroup", map[string]interface{}{
				"GroupId": groupID,
			})
			if err != nil {
				return err
			}

			output.PrintSuccess(fmt.Sprintf("机器组 %s 已删除", groupID))
			return nil
		},
	}

	cmd.Flags().StringVar(&groupID, "id", "", "机器组 ID（必填）")
	_ = cmd.MarkFlagRequired("id")
	return cmd
}

func newInfoCmd(f *cmdutil.Factory) *cobra.Command {
	var groupID string

	cmd := &cobra.Command{
		Use:   "+info",
		Short: "查看机器组详情",
		RunE: func(cmd *cobra.Command, args []string) error {
			if groupID == "" {
				return fmt.Errorf("--id 参数必填")
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			result, err := clsClient.Call("DescribeMachineGroupConfigs", map[string]interface{}{
				"GroupId": groupID,
			})
			if err != nil {
				return err
			}

			output.FormatOutput(result, f.Format)
			return nil
		},
	}

	cmd.Flags().StringVar(&groupID, "id", "", "机器组 ID（必填）")
	_ = cmd.MarkFlagRequired("id")
	return cmd
}

func newStatusCmd(f *cmdutil.Factory) *cobra.Command {
	var groupID string

	cmd := &cobra.Command{
		Use:   "+status",
		Short: "查看机器组中机器状态",
		Long: `查看机器组下各台机器的 LogListener 状态。

示例:
  cls-cli machinegroup +status --id <group_id>`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if groupID == "" {
				return fmt.Errorf("--id 参数必填")
			}

			clsClient, err := f.CLSClient()
			if err != nil {
				return err
			}

			result, err := clsClient.Call("DescribeMachines", map[string]interface{}{
				"GroupId": groupID,
			})
			if err != nil {
				return err
			}

			formatMachineStatus(result, f.Format, f.IOStreams)
			return nil
		},
	}

	cmd.Flags().StringVar(&groupID, "id", "", "机器组 ID（必填）")
	_ = cmd.MarkFlagRequired("id")
	return cmd
}

// --- helpers ---

func formatMachineGroupList(data map[string]interface{}, format output.Format, streams *cmdutil.IOStreams) {
	resp, ok := data["Response"].(map[string]interface{})
	if !ok {
		output.FormatOutput(data, format)
		return
	}

	groups, ok := resp["MachineGroups"].([]interface{})
	if !ok || len(groups) == 0 {
		fmt.Fprintln(streams.ErrOut, "暂无机器组")
		return
	}

	if format == output.FormatTable || format == output.FormatCSV {
		rows := make([]map[string]interface{}, 0, len(groups))
		for _, g := range groups {
			if m, ok := g.(map[string]interface{}); ok {
				rows = append(rows, map[string]interface{}{
					"GroupId":   m["GroupId"],
					"GroupName": m["GroupName"],
					"CreateTime": m["CreateTime"],
				})
			}
		}
		output.FormatOutput(rows, format)
	} else {
		output.FormatOutput(resp, format)
	}
}

func formatMachineStatus(data map[string]interface{}, format output.Format, streams *cmdutil.IOStreams) {
	resp, ok := data["Response"].(map[string]interface{})
	if !ok {
		output.FormatOutput(data, format)
		return
	}

	machines, ok := resp["Machines"].([]interface{})
	if !ok || len(machines) == 0 {
		fmt.Fprintln(streams.ErrOut, "该机器组暂无机器")
		return
	}

	if format == output.FormatTable || format == output.FormatCSV {
		rows := make([]map[string]interface{}, 0, len(machines))
		for _, m := range machines {
			if machine, ok := m.(map[string]interface{}); ok {
				status := "异常"
				if s, ok := machine["Status"].(float64); ok && s == 0 {
					status = "正常"
				}
				rows = append(rows, map[string]interface{}{
					"IP":      machine["Ip"],
					"Status":  status,
					"Version": machine["Version"],
				})
			}
		}
		output.FormatOutput(rows, format)
	} else {
		output.FormatOutput(resp, format)
	}
}
