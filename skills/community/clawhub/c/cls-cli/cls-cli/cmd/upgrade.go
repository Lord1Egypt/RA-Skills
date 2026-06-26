package cmd

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"runtime"
	"strings"
	"time"

	"github.com/spf13/cobra"
)

const (
	Version   = "0.2.0"
	repoOwner = "trumphuang"
	repoName  = "CLS_CLI"
)

type githubRelease struct {
	TagName string        `json:"tag_name"`
	Assets  []githubAsset `json:"assets"`
}

type githubAsset struct {
	Name               string `json:"name"`
	BrowserDownloadURL string `json:"browser_download_url"`
}

func newUpgradeCmd() *cobra.Command {
	var force bool

	cmd := &cobra.Command{
		Use:   "upgrade",
		Short: "升级 cls-cli 到最新版本",
		Long: `从 GitHub Release 下载并安装最新版本的 cls-cli。

升级流程：
  1. 检查 GitHub 上的最新版本
  2. 如果有新版本，下载对应平台的二进制文件
  3. 替换当前的 cls-cli 可执行文件

示例:
  cls-cli upgrade              # 检查并升级到最新版
  cls-cli upgrade --force      # 强制重新安装（即使已是最新版）`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runUpgrade(force)
		},
	}

	cmd.Flags().BoolVar(&force, "force", false, "强制重新安装，即使已是最新版")
	return cmd
}

func runUpgrade(force bool) error {
	fmt.Printf("当前版本: v%s\n", Version)
	fmt.Println("正在检查最新版本...")

	latest, err := getLatestRelease()
	if err != nil {
		return fmt.Errorf("检查最新版本失败: %w\n\n手动升级方式:\n  git clone https://github.com/%s/%s.git\n  cd %s/cls-cli && go build -o cls-cli . && sudo mv cls-cli /usr/local/bin/", repoOwner, repoName, repoName)
	}

	latestVersion := strings.TrimPrefix(latest.TagName, "v")
	fmt.Printf("最新版本: v%s\n", latestVersion)

	if !force && latestVersion == Version {
		fmt.Println("已经是最新版本，无需升级。")
		fmt.Println("如需强制重新安装，请使用: cls-cli upgrade --force")
		return nil
	}

	// 确定当前平台
	goos := runtime.GOOS
	goarch := runtime.GOARCH
	assetName := fmt.Sprintf("cls-cli-%s-%s", goos, goarch)

	// 在 release assets 中查找对应平台的二进制
	var downloadURL string
	for _, asset := range latest.Assets {
		if asset.Name == assetName || asset.Name == assetName+".tar.gz" || asset.Name == assetName+".zip" {
			downloadURL = asset.BrowserDownloadURL
			break
		}
	}

	// 如果没有预编译二进制，走源码编译
	if downloadURL == "" {
		fmt.Printf("未找到 %s/%s 的预编译二进制，尝试从源码构建...\n", goos, goarch)
		return upgradeFromSource()
	}

	return upgradeFromBinary(downloadURL, assetName)
}

func getLatestRelease() (*githubRelease, error) {
	url := fmt.Sprintf("https://api.github.com/repos/%s/%s/releases/latest", repoOwner, repoName)
	client := &http.Client{Timeout: 15 * time.Second}
	resp, err := client.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode == 404 {
		// 没有 release，返回一个空的让它走源码编译
		return &githubRelease{TagName: "v99.0.0"}, nil
	}

	if resp.StatusCode != 200 {
		return nil, fmt.Errorf("GitHub API 返回 %d", resp.StatusCode)
	}

	var release githubRelease
	if err := json.NewDecoder(resp.Body).Decode(&release); err != nil {
		return nil, err
	}
	return &release, nil
}

func upgradeFromSource() error {
	fmt.Println("正在从 GitHub 拉取最新源码并编译...")

	// 检查 go 是否可用
	if _, err := exec.LookPath("go"); err != nil {
		return fmt.Errorf("未找到 go 编译器，请先安装 Go: https://go.dev/dl/\n\n或手动升级:\n  git clone https://github.com/%s/%s.git\n  cd %s/cls-cli && go build -o cls-cli . && sudo mv cls-cli /usr/local/bin/", repoOwner, repoName, repoName)
	}

	// 检查 git 是否可用
	if _, err := exec.LookPath("git"); err != nil {
		return fmt.Errorf("未找到 git，请先安装 git")
	}

	// 创建临时目录
	tmpDir, err := os.MkdirTemp("", "cls-cli-upgrade-*")
	if err != nil {
		return fmt.Errorf("创建临时目录失败: %w", err)
	}
	defer os.RemoveAll(tmpDir)

	// git clone
	fmt.Println("  -> git clone ...")
	cloneCmd := exec.Command("git", "clone", "--depth", "1",
		fmt.Sprintf("https://github.com/%s/%s.git", repoOwner, repoName), tmpDir)
	cloneCmd.Stdout = os.Stdout
	cloneCmd.Stderr = os.Stderr
	if err := cloneCmd.Run(); err != nil {
		return fmt.Errorf("git clone 失败: %w", err)
	}

	// go build
	fmt.Println("  -> go build ...")
	buildDir := tmpDir + "/cls-cli"
	buildCmd := exec.Command("go", "build", "-o", "cls-cli", ".")
	buildCmd.Dir = buildDir
	buildCmd.Stdout = os.Stdout
	buildCmd.Stderr = os.Stderr
	if err := buildCmd.Run(); err != nil {
		return fmt.Errorf("编译失败: %w", err)
	}

	// 获取当前可执行文件路径
	currentBin, err := os.Executable()
	if err != nil {
		currentBin = "/usr/local/bin/cls-cli"
	}

	// 复制新二进制到目标位置
	newBin := buildDir + "/cls-cli"
	fmt.Printf("  -> 安装到 %s ...\n", currentBin)

	if err := copyFile(newBin, currentBin); err != nil {
		// 可能需要 sudo
		fmt.Printf("直接写入失败，尝试 sudo ...\n")
		sudoCmd := exec.Command("sudo", "cp", newBin, currentBin)
		sudoCmd.Stdin = os.Stdin
		sudoCmd.Stdout = os.Stdout
		sudoCmd.Stderr = os.Stderr
		if err := sudoCmd.Run(); err != nil {
			return fmt.Errorf("安装失败: %w\n\n请手动执行:\n  sudo cp %s %s", err, newBin, currentBin)
		}
	}

	fmt.Println("\n✅ 升级成功！")
	// 打印新版本
	verCmd := exec.Command(currentBin, "version")
	verCmd.Stdout = os.Stdout
	verCmd.Stderr = os.Stderr
	_ = verCmd.Run()

	return nil
}

func upgradeFromBinary(downloadURL, assetName string) error {
	fmt.Printf("正在下载 %s ...\n", assetName)

	client := &http.Client{Timeout: 120 * time.Second}
	resp, err := client.Get(downloadURL)
	if err != nil {
		return fmt.Errorf("下载失败: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return fmt.Errorf("下载失败，HTTP %d", resp.StatusCode)
	}

	// 写入临时文件
	tmpFile, err := os.CreateTemp("", "cls-cli-*")
	if err != nil {
		return fmt.Errorf("创建临时文件失败: %w", err)
	}
	tmpPath := tmpFile.Name()
	defer os.Remove(tmpPath)

	if _, err := io.Copy(tmpFile, resp.Body); err != nil {
		tmpFile.Close()
		return fmt.Errorf("写入失败: %w", err)
	}
	tmpFile.Close()

	// 设置可执行权限
	if err := os.Chmod(tmpPath, 0755); err != nil {
		return fmt.Errorf("设置权限失败: %w", err)
	}

	// 获取当前可执行文件路径
	currentBin, err := os.Executable()
	if err != nil {
		currentBin = "/usr/local/bin/cls-cli"
	}

	fmt.Printf("正在安装到 %s ...\n", currentBin)

	if err := copyFile(tmpPath, currentBin); err != nil {
		sudoCmd := exec.Command("sudo", "cp", tmpPath, currentBin)
		sudoCmd.Stdin = os.Stdin
		sudoCmd.Stdout = os.Stdout
		sudoCmd.Stderr = os.Stderr
		if err := sudoCmd.Run(); err != nil {
			return fmt.Errorf("安装失败: %w", err)
		}
	}

	fmt.Println("\n✅ 升级成功！")
	verCmd := exec.Command(currentBin, "version")
	verCmd.Stdout = os.Stdout
	verCmd.Stderr = os.Stderr
	_ = verCmd.Run()

	return nil
}

func copyFile(src, dst string) error {
	in, err := os.Open(src)
	if err != nil {
		return err
	}
	defer in.Close()

	out, err := os.OpenFile(dst, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0755)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, in)
	return err
}
