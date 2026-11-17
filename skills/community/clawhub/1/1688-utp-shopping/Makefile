# Makefile — UTP Skill 构建与发布
#
# 用法:
#   make publish                    # 发布 patch 版本 (自动 +0.0.1)
#   make publish VERSION=1.1.0      # 发布指定版本
#   make bump                       # 仅升版本号,不发布
#   make check                      # 脚本语法检查
#   make package                    # 打公网 zip 包

SHELL := /bin/bash
SKILL_DIR := $(shell pwd)
SKILL_MD := $(SKILL_DIR)/SKILL.md
INSTALL_SH := $(SKILL_DIR)/scripts/install.sh
INSTALL_WIN_SH := $(SKILL_DIR)/scripts/install-win.sh
OUT_DIR := $(HOME)/Documents

# 当前版本(从 SKILL.md frontmatter 读取)
CURRENT_VERSION := $(shell grep '^version:' $(SKILL_MD) | head -1 | sed 's/version: *//')

# 目标版本:用户指定 > 自动 patch +1
ifdef VERSION
  NEXT_VERSION := $(VERSION)
else
  NEXT_VERSION := $(shell echo $(CURRENT_VERSION) | awk -F. '{print $$1"."$$2"."$$3+1}')
endif

TMP_DIR := $(shell mktemp -d /tmp/utp-skill-pkg.XXXXXX)
# 发布包统一收口：包名、解压文件夹、skill 名三者一致，均为 utp-shopping
PKG_NAME := utp-shopping
ZIP_FILE := $(OUT_DIR)/utp-shopping.zip

.PHONY: publish bump check package help

help: ## 显示帮助
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[1m%-18s\033[0m %s\n", $$1, $$2}'

check: ## 脚本语法检查
	@echo "检查 install.sh 语法..."
	@bash -n $(INSTALL_SH) && echo "  ✓ install.sh OK"
	@echo "检查 install-win.sh 语法..."
	@bash -n $(INSTALL_WIN_SH) && echo "  ✓ install-win.sh OK"
	@echo "检查 SKILL.md frontmatter..."
	@grep -q '^name:' $(SKILL_MD) && grep -q '^version:' $(SKILL_MD) && echo "  ✓ SKILL.md frontmatter OK"

bump: check ## 升版本号到 SKILL.md
	@echo "升版本: $(CURRENT_VERSION) → $(NEXT_VERSION)"
	@sed -i '' 's/^version: $(CURRENT_VERSION)/version: $(NEXT_VERSION)/' $(SKILL_MD)
	@echo "  ✓ 版本已更新到 $(NEXT_VERSION)"

package: check ## 打公网 zip 包（输出到 ~/Documents/）
	@echo "打包: $(PKG_NAME).zip"
	@rm -rf "$(TMP_DIR)/$(PKG_NAME)"
	@mkdir -p "$(TMP_DIR)/$(PKG_NAME)"
	@cp $(SKILL_MD) "$(TMP_DIR)/$(PKG_NAME)/"
	@cp README.md "$(TMP_DIR)/$(PKG_NAME)/"
	@cp LICENSE "$(TMP_DIR)/$(PKG_NAME)/"
	@cp package_back.json "$(TMP_DIR)/$(PKG_NAME)/package.json"
	@# package.json 版本以 SKILL.md frontmatter 为单一事实源，打包时同步注入
	@sed -i '' 's/"version": *"[^"]*"/"version": "$(CURRENT_VERSION)"/' "$(TMP_DIR)/$(PKG_NAME)/package.json"
	@cp .npmignore "$(TMP_DIR)/$(PKG_NAME)/"
	@cp -R scripts "$(TMP_DIR)/$(PKG_NAME)/"
	@cp -R references "$(TMP_DIR)/$(PKG_NAME)/"
	@cp dsh.cordis.yml dsh-apps.cordis.yml "$(TMP_DIR)/$(PKG_NAME)/"
	@rm -rf "$(TMP_DIR)/$(PKG_NAME)/scripts"/.git
	@mkdir -p "$(OUT_DIR)"
	@rm -f "$(ZIP_FILE)"
	@cd "$(TMP_DIR)" && zip -r "$(ZIP_FILE)" "$(PKG_NAME)" -x "*.DS_Store"
	@rm -rf "$(TMP_DIR)"
	@echo ""
	@echo "  ✓ $(ZIP_FILE)"
	@echo ""
	@echo "包含文件:"
	@unzip -l "$(ZIP_FILE)" | tail -n +4 | sed '$$d' | sed '$$d'

publish: bump ## 升版本 + 提交 + 打 tag + 推送
	@echo ""
	@echo "提交变更..."
	@git add $(SKILL_MD) $(INSTALL_SH) $(INSTALL_WIN_SH) README.md references/ scripts/ .npmignore
	@git diff --cached --quiet && { echo "  ⚠ 没有需要提交的变更"; exit 0; } || true
	@git commit -m "chore(release): v$(NEXT_VERSION)"
	@echo "  ✓ 已提交"
	@echo ""
	@echo "打 tag..."
	@git tag -a "v$(NEXT_VERSION)" -m "v$(NEXT_VERSION)"
	@echo "  ✓ 已打 tag v$(NEXT_VERSION)"
	@echo ""
	@echo "推送到远程..."
	@git push origin master --tags
	@echo "  ✓ 已推送"
	@echo ""
	@echo "发布完成: v$(NEXT_VERSION)"
