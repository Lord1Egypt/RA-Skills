package loglistener

import (
	"fmt"
	"runtime"
	"strings"

	"github.com/spf13/cobra"
	"github.com/tencentcloud/cls-cli/internal/cmdutil"
)

func RegisterShortcuts(rootCmd *cobra.Command, f *cmdutil.Factory) {
	llCmd := &cobra.Command{
		Use:   "loglistener",
		Short: "LogListener 采集器管理",
		Long: `LogListener 采集器的安装、初始化、启停管理。

LogListener 是腾讯云 CLS 的日志采集 Agent，部署在需要采集日志的服务器上，
负责将服务器上的日志实时采集并上报到 CLS。

常用流程：
  1. cls-cli loglistener +install         # 安装 LogListener
  2. cls-cli loglistener +init            # 初始化（配置 AK/SK/Region）
  3. cls-cli loglistener +start           # 启动服务
  4. cls-cli machinegroup +create         # 创建机器组
  5. cls-cli collector +create            # 创建采集配置`,
		Aliases: []string{"ll"},
	}

	llCmd.AddCommand(newInstallCmd(f))
	llCmd.AddCommand(newInitCmd(f))
	llCmd.AddCommand(newStartCmd())
	llCmd.AddCommand(newStopCmd())
	llCmd.AddCommand(newRestartCmd())
	llCmd.AddCommand(newStatusCmd())
	llCmd.AddCommand(newUninstallCmd())
	llCmd.AddCommand(newCheckCmd())

	rootCmd.AddCommand(llCmd)
}

// +install: 生成安装 LogListener 的脚本命令
func newInstallCmd(f *cmdutil.Factory) *cobra.Command {
	var (
		arch     string
		network  string
		version  string
		path     string
	)

	cmd := &cobra.Command{
		Use:   "+install",
		Short: "安装 LogListener 采集器",
		Long: `生成并展示 LogListener 的安装命令。

支持 x64 和 ARM 架构，支持内网和外网下载。

示例:
  # 默认安装（x64 外网）
  cls-cli loglistener +install

  # ARM 架构内网安装
  cls-cli loglistener +install --arch arm --network intra

  # 指定版本安装
  cls-cli loglistener +install --version 2.9.0

  # 指定安装路径
  cls-cli loglistener +install --path /opt/`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if arch == "" {
				if runtime.GOARCH == "arm64" || runtime.GOARCH == "arm" {
					arch = "arm"
				} else {
					arch = "x64"
				}
			}

			var baseURL string
			if network == "intra" {
				baseURL = "http://mirrors.tencentyun.com/install/cls"
			} else {
				baseURL = "http://mirrors.tencent.com/install/cls"
			}

			var pkg string
			if strings.ToLower(arch) == "arm" {
				if version != "" {
					pkg = fmt.Sprintf("loglistener-linux-ARM-%s.tar.gz", version)
				} else {
					pkg = "loglistener-linux-ARM-2.9.0.tar.gz"
				}
			} else {
				if version != "" {
					pkg = fmt.Sprintf("loglistener-linux-x64-%s.tar.gz", version)
				} else {
					pkg = "loglistener-linux-x64.tar.gz"
				}
			}

			downloadURL := fmt.Sprintf("%s/%s", baseURL, pkg)

			script := fmt.Sprintf(`#!/bin/bash
# LogListener 安装脚本
# 架构: %s | 网络: %s | 安装路径: %s

set -e

echo ">>> 下载 LogListener..."
wget %s -O /tmp/%s

echo ">>> 解压到 %s ..."
tar zxvf /tmp/%s -C %s

echo ">>> 执行安装..."
cd %sloglistener/tools && ./loglistener.sh install

echo ">>> 安装完成！"
echo ""
echo "下一步："
echo "  1. 初始化: cls-cli loglistener +init --region <region>"
echo "  2. 启动:   cls-cli loglistener +start"
echo "  3. 检查:   cls-cli loglistener +status"
`, arch, network, path, downloadURL, pkg, path, pkg, path, path)

			fmt.Fprintln(f.IOStreams.Out, script)

			fmt.Fprintln(f.IOStreams.ErrOut, "提示: 复制上面的脚本到目标服务器执行，或直接运行：")
			fmt.Fprintf(f.IOStreams.ErrOut, "  wget %s && tar zxvf %s -C %s && cd %sloglistener/tools && ./loglistener.sh install\n", downloadURL, pkg, path, path)

			return nil
		},
	}

	cmd.Flags().StringVar(&arch, "arch", "", "处理器架构: x64, arm（默认自动检测）")
	cmd.Flags().StringVar(&network, "network", "internet", "下载网络: internet（外网）, intra（内网）")
	cmd.Flags().StringVar(&version, "version", "", "指定版本号（默认最新版）")
	cmd.Flags().StringVar(&path, "path", "/usr/local/", "安装路径")
	return cmd
}

// +init: 生成初始化 LogListener 的命令
func newInitCmd(f *cmdutil.Factory) *cobra.Command {
	var (
		region     string
		network    string
		ip         string
		label      string
		encryption bool
		path       string
	)

	cmd := &cobra.Command{
		Use:   "+init",
		Short: "初始化 LogListener",
		Long: `生成 LogListener 初始化命令，配置密钥和地域信息。

会自动读取 cls-cli 中已配置的 AK/SK，无需重复输入。

示例:
  # 使用 cls-cli 已配置的密钥（内网）
  cls-cli loglistener +init --region ap-guangzhou

  # 外网模式
  cls-cli loglistener +init --region ap-guangzhou --network internet

  # 指定机器标识
  cls-cli loglistener +init --region ap-guangzhou --label "webserver,group1"

  # 指定机器 IP
  cls-cli loglistener +init --region ap-guangzhou --ip 10.0.0.1`,
		RunE: func(cmd *cobra.Command, args []string) error {
			if region == "" {
				return fmt.Errorf("--region 参数必填，例如 ap-guangzhou, ap-beijing")
			}

			cfg, err := f.Config()
			if err != nil {
				return fmt.Errorf("读取配置失败，请先运行 cls-cli config init: %w", err)
			}

			initCmd := fmt.Sprintf("cd %sloglistener/tools && ./loglistener.sh init -secretid %s -secretkey %s -region %s -network %s",
				path, cfg.SecretID, cfg.SecretKey, region, network)

			if ip != "" {
				initCmd += fmt.Sprintf(" -ip %s", ip)
			}
			if label != "" {
				initCmd += fmt.Sprintf(" -label \"%s\"", label)
			}
			if encryption {
				initCmd += " -encryption true"
			}

			fmt.Fprintln(f.IOStreams.Out, "# LogListener 初始化命令")
			fmt.Fprintln(f.IOStreams.Out, initCmd)
			fmt.Fprintln(f.IOStreams.Out, "")
			fmt.Fprintln(f.IOStreams.ErrOut, "提示: 复制上面的命令到已安装 LogListener 的服务器执行")

			return nil
		},
	}

	cmd.Flags().StringVar(&region, "region", "", "日志服务地域（必填），如 ap-guangzhou")
	cmd.Flags().StringVar(&network, "network", "intra", "网络类型: intra（内网）, internet（外网）")
	cmd.Flags().StringVar(&ip, "ip", "", "机器 IP（不填则自动获取）")
	cmd.Flags().StringVar(&label, "label", "", "机器标识，多个用逗号分隔")
	cmd.Flags().BoolVar(&encryption, "encryption", false, "是否加密存储密钥")
	cmd.Flags().StringVar(&path, "path", "/usr/local/", "LogListener 安装路径")
	_ = cmd.MarkFlagRequired("region")
	return cmd
}

// +start
func newStartCmd() *cobra.Command {
	var useSystemd bool

	cmd := &cobra.Command{
		Use:   "+start",
		Short: "启动 LogListener 服务",
		Long: `生成启动 LogListener 的命令。

示例:
  cls-cli loglistener +start
  cls-cli loglistener +start --systemd`,
		Run: func(cmd *cobra.Command, args []string) {
			if useSystemd {
				fmt.Println("systemctl start loglistenerd")
			} else {
				fmt.Println("/etc/init.d/loglistenerd start")
			}
		},
	}

	cmd.Flags().BoolVar(&useSystemd, "systemd", true, "使用 systemd 管理（推荐，默认开启）")
	return cmd
}

// +stop
func newStopCmd() *cobra.Command {
	var useSystemd bool

	cmd := &cobra.Command{
		Use:   "+stop",
		Short: "停止 LogListener 服务",
		Run: func(cmd *cobra.Command, args []string) {
			if useSystemd {
				fmt.Println("systemctl stop loglistenerd")
			} else {
				fmt.Println("/etc/init.d/loglistenerd stop")
			}
		},
	}

	cmd.Flags().BoolVar(&useSystemd, "systemd", true, "使用 systemd 管理")
	return cmd
}

// +restart
func newRestartCmd() *cobra.Command {
	var useSystemd bool

	cmd := &cobra.Command{
		Use:   "+restart",
		Short: "重启 LogListener 服务",
		Run: func(cmd *cobra.Command, args []string) {
			if useSystemd {
				fmt.Println("systemctl restart loglistenerd")
			} else {
				fmt.Println("/etc/init.d/loglistenerd restart")
			}
		},
	}

	cmd.Flags().BoolVar(&useSystemd, "systemd", true, "使用 systemd 管理")
	return cmd
}

// +status
func newStatusCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "+status",
		Short: "查看 LogListener 运行状态",
		Long: `生成查看 LogListener 状态的命令。

正常运行时应有两个进程。`,
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Println("# 查看 LogListener 状态")
			fmt.Println("/etc/init.d/loglistenerd status")
			fmt.Println("")
			fmt.Println("# 检查心跳和配置")
			fmt.Println("/etc/init.d/loglistenerd check")
			fmt.Println("")
			fmt.Println("# 查看版本")
			fmt.Println("/etc/init.d/loglistenerd -v")
		},
	}
	return cmd
}

// +uninstall
func newUninstallCmd() *cobra.Command {
	var path string

	cmd := &cobra.Command{
		Use:   "+uninstall",
		Short: "卸载 LogListener",
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Printf("cd %sloglistener/tools && ./loglistener.sh uninstall\n", path)
		},
	}

	cmd.Flags().StringVar(&path, "path", "/usr/local/", "LogListener 安装路径")
	return cmd
}

// +check
func newCheckCmd() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "+check",
		Short: "检查 LogListener 心跳和配置",
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Println("/etc/init.d/loglistenerd check")
		},
	}
	return cmd
}
