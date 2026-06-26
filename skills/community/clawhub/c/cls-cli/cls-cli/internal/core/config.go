package core

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

// CliConfig holds the runtime configuration for CLS CLI.
type CliConfig struct {
	SecretID  string `json:"secret_id"`
	SecretKey string `json:"secret_key"`
	Region    string `json:"region"`
	Endpoint  string `json:"endpoint,omitempty"`
}

func GetConfigDir() string {
	if dir := os.Getenv("CLS_CLI_CONFIG_DIR"); dir != "" {
		return dir
	}
	home, err := os.UserHomeDir()
	if err != nil {
		return ".cls-cli"
	}
	return filepath.Join(home, ".cls-cli")
}

func GetConfigPath() string {
	return filepath.Join(GetConfigDir(), "config.json")
}

func LoadConfig() (*CliConfig, error) {
	path := GetConfigPath()
	data, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, fmt.Errorf("未找到配置文件，请先运行 cls-cli config init")
		}
		return nil, err
	}
	var cfg CliConfig
	if err := json.Unmarshal(data, &cfg); err != nil {
		return nil, fmt.Errorf("配置文件格式错误: %w", err)
	}
	if envID := os.Getenv("TENCENTCLOUD_SECRET_ID"); envID != "" {
		cfg.SecretID = envID
	}
	if envKey := os.Getenv("TENCENTCLOUD_SECRET_KEY"); envKey != "" {
		cfg.SecretKey = envKey
	}
	if envRegion := os.Getenv("CLS_DEFAULT_REGION"); envRegion != "" {
		cfg.Region = envRegion
	}
	if cfg.SecretID == "" || cfg.SecretKey == "" {
		return nil, fmt.Errorf("SecretID 或 SecretKey 未配置，请运行 cls-cli config init")
	}
	return &cfg, nil
}

func SaveConfig(cfg *CliConfig) error {
	dir := GetConfigDir()
	if err := os.MkdirAll(dir, 0700); err != nil {
		return err
	}
	data, err := json.MarshalIndent(cfg, "", "  ")
	if err != nil {
		return err
	}
	path := GetConfigPath()
	tmpPath := path + ".tmp"
	if err := os.WriteFile(tmpPath, data, 0600); err != nil {
		return err
	}
	return os.Rename(tmpPath, path)
}
