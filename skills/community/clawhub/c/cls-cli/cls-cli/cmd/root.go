package cmd

import (
	"fmt"
	"os"
	"runtime"

	"github.com/spf13/cobra"
	"github.com/tencentcloud/cls-cli/cmd/api"
	"github.com/tencentcloud/cls-cli/cmd/config"
	"github.com/tencentcloud/cls-cli/internal/cmdutil"
	"github.com/tencentcloud/cls-cli/internal/output"
	"github.com/tencentcloud/cls-cli/shortcuts/alarm"
	"github.com/tencentcloud/cls-cli/shortcuts/collector"
	"github.com/tencentcloud/cls-cli/shortcuts/dashboard"
	"github.com/tencentcloud/cls-cli/shortcuts/log"
	"github.com/tencentcloud/cls-cli/shortcuts/loglistener"
	"github.com/tencentcloud/cls-cli/shortcuts/machinegroup"
	"github.com/tencentcloud/cls-cli/shortcuts/topic"
)

func Execute() int {
	f := cmdutil.NewDefault()

	rootCmd := &cobra.Command{
		Use:   "cls-cli",
		Short: "腾讯云日志服务 CLS 命令行工具",
		Long: `cls-cli 是腾讯云日志服务(CLS)的命令行工具，
支持日志检索、主题管理、告警管理等核心功能。

面向人类和 AI Agent，提供三层命令架构：
  Layer 1: 快捷命令   cls-cli log +search --topic xxx --query "error"
  Layer 2: 通用API    cls-cli api SearchLog --params '{...}'`,
		SilenceUsage:  true,
		SilenceErrors: true,
	}

	var formatStr string
	rootCmd.PersistentFlags().StringVar(&formatStr, "format", "json", "输出格式: json, pretty, table, csv")
	rootCmd.PersistentFlags().BoolVar(&f.DryRun, "dry-run", false, "预览模式，不实际执行")
	rootCmd.PersistentFlags().BoolVarP(&f.ForceYes, "yes", "y", false, "跳过危险操作的二次确认")
	rootCmd.PersistentFlags().StringVar(&f.RegionOverride, "region", "", "指定地域（优先级最高，覆盖配置文件和环境变量），如 ap-guangzhou, ap-beijing")

	cobra.OnInitialize(func() {
		f.Format = output.ParseFormat(formatStr)
	})

	rootCmd.AddCommand(config.NewCmdConfig(f))
	rootCmd.AddCommand(api.NewCmdApi(f))

	log.RegisterShortcuts(rootCmd, f)
	topic.RegisterShortcuts(rootCmd, f)
	alarm.RegisterShortcuts(rootCmd, f)
	loglistener.RegisterShortcuts(rootCmd, f)
	machinegroup.RegisterShortcuts(rootCmd, f)
	collector.RegisterShortcuts(rootCmd, f)
	dashboard.RegisterShortcuts(rootCmd, f)

	rootCmd.AddCommand(newVersionCmd())
	rootCmd.AddCommand(newUpgradeCmd())

	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %s\n", err)
		return 1
	}
	return 0
}

func newVersionCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "version",
		Short: "显示版本信息",
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Printf("cls-cli version %s (%s/%s)\n", Version, runtime.GOOS, runtime.GOARCH)
		},
	}
}
