package cmdutil

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
	"sync"

	"github.com/tencentcloud/cls-cli/internal/client"
	"github.com/tencentcloud/cls-cli/internal/core"
	"github.com/tencentcloud/cls-cli/internal/output"
)

type IOStreams struct {
	In     io.Reader
	Out    io.Writer
	ErrOut io.Writer
}

type Factory struct {
	Config         func() (*core.CliConfig, error)
	CLSClient      func() (*client.APIClient, error)
	IOStreams       *IOStreams
	Format         output.Format
	DryRun         bool
	ForceYes       bool   // --yes 跳过删除等危险操作的二次确认
	RegionOverride string // --region 全局参数，优先级最高
}

// ConfirmAction 对危险操作进行二次确认，返回 true 表示用户确认执行。
// 如果 ForceYes 为 true（传了 --yes），直接返回 true。
func (f *Factory) ConfirmAction(message string) bool {
	if f.ForceYes {
		return true
	}
	fmt.Fprintf(f.IOStreams.ErrOut, "⚠️  %s\n", message)
	fmt.Fprint(f.IOStreams.ErrOut, "确认请输入 yes: ")
	reader := bufio.NewReader(f.IOStreams.In)
	input, _ := reader.ReadString('\n')
	return strings.TrimSpace(input) == "yes"
}

func NewDefault() *Factory {
	streams := &IOStreams{
		In:     os.Stdin,
		Out:    os.Stdout,
		ErrOut: os.Stderr,
	}

	var (
		cfgOnce    sync.Once
		cfgVal     *core.CliConfig
		cfgErr     error
		clientOnce sync.Once
		clientVal  *client.APIClient
		clientErr  error
	)

	configFn := func() (*core.CliConfig, error) {
		cfgOnce.Do(func() {
			cfgVal, cfgErr = core.LoadConfig()
		})
		return cfgVal, cfgErr
	}

	f := &Factory{
		IOStreams: streams,
	}

	clientFn := func() (*client.APIClient, error) {
		clientOnce.Do(func() {
			cfg, err := configFn()
			if err != nil {
				clientErr = err
				return
			}
			region := cfg.Region
			if f.RegionOverride != "" {
				region = f.RegionOverride
			}
			clientVal = client.NewAPIClient(cfg.SecretID, cfg.SecretKey, region, cfg.Endpoint)
		})
		return clientVal, clientErr
	}

	f.Config = configFn
	f.CLSClient = clientFn
	return f
}
