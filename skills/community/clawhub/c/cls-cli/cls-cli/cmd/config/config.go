package config

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"github.com/spf13/cobra"
	"github.com/tencentcloud/cls-cli/internal/cmdutil"
	"github.com/tencentcloud/cls-cli/internal/core"
	"github.com/tencentcloud/cls-cli/internal/output"
)

func NewCmdConfig(f *cmdutil.Factory) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "config",
		Short: "配置管理",
		Long:  "管理 cls-cli 的认证配置和默认参数",
	}

	cmd.AddCommand(newCmdConfigInit(f))
	cmd.AddCommand(newCmdConfigShow(f))
	return cmd
}

func newCmdConfigInit(f *cmdutil.Factory) *cobra.Command {
	var (
		secretID  string
		secretKey string
		region    string
	)

	cmd := &cobra.Command{
		Use:   "init",
		Short: "初始化配置（设置 SecretId、SecretKey、Region）",
		Long: `交互式或通过参数配置腾讯云 API 凭证。

示例:
  # 交互式配置
  cls-cli config init

  # 直接传参
  cls-cli config init --secret-id AKIDxxx --secret-key yyy --region ap-guangzhou`,
		RunE: func(cmd *cobra.Command, args []string) error {
			reader := bufio.NewReader(os.Stdin)

			if secretID == "" {
				fmt.Print("SecretId: ")
				input, _ := reader.ReadString('\n')
				secretID = strings.TrimSpace(input)
			}
			if secretKey == "" {
				fmt.Print("SecretKey: ")
				input, _ := reader.ReadString('\n')
				secretKey = strings.TrimSpace(input)
			}
			if region == "" {
				fmt.Print("默认 Region (如 ap-guangzhou): ")
				input, _ := reader.ReadString('\n')
				region = strings.TrimSpace(input)
				if region == "" {
					region = "ap-guangzhou"
				}
			}

			if secretID == "" || secretKey == "" {
				return fmt.Errorf("SecretId 和 SecretKey 不能为空")
			}

			cfg := &core.CliConfig{
				SecretID:  secretID,
				SecretKey: secretKey,
				Region:    region,
			}

			if err := core.SaveConfig(cfg); err != nil {
				return fmt.Errorf("保存配置失败: %w", err)
			}

			output.PrintSuccess(fmt.Sprintf("配置已保存到 %s", core.GetConfigPath()))
			return nil
		},
	}

	cmd.Flags().StringVar(&secretID, "secret-id", "", "腾讯云 SecretId")
	cmd.Flags().StringVar(&secretKey, "secret-key", "", "腾讯云 SecretKey")
	cmd.Flags().StringVar(&region, "region", "", "默认 Region (如 ap-guangzhou)")
	return cmd
}

func newCmdConfigShow(f *cmdutil.Factory) *cobra.Command {
	return &cobra.Command{
		Use:   "show",
		Short: "显示当前配置",
		RunE: func(cmd *cobra.Command, args []string) error {
			cfg, err := f.Config()
			if err != nil {
				return err
			}
			masked := &core.CliConfig{
				SecretID:  maskSecret(cfg.SecretID),
				SecretKey: maskSecret(cfg.SecretKey),
				Region:    cfg.Region,
				Endpoint:  cfg.Endpoint,
			}
			output.FormatOutput(map[string]interface{}{
				"secret_id":  masked.SecretID,
				"secret_key": masked.SecretKey,
				"region":     masked.Region,
				"endpoint":   masked.Endpoint,
				"config_dir": core.GetConfigDir(),
			}, f.Format)
			return nil
		},
	}
}

func maskSecret(s string) string {
	if len(s) <= 8 {
		return "****"
	}
	return s[:4] + strings.Repeat("*", len(s)-8) + s[len(s)-4:]
}
