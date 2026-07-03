# ---------------------------------------------------------------------------
# Makefile — plan, apply, destroy, output targets
# ---------------------------------------------------------------------------

SHELL          := /bin/bash
TF             ?= terraform
TF_DIR         ?= .
AUTO_APPROVE   ?= ""
PROJECT_ID     ?= evez-mesh-prod
REGION         ?= us-west1

# Terraform initialization
.PHONY: init
init:
	$(TF) -chdir=$(TF_DIR) init -upgrade

# Format check
.PHONY: fmt
fmt:
	$(TF) -chdir=$(TF_DIR) fmt -recursive -diff

# Validate configuration
.PHONY: validate
validate: init
	$(TF) -chdir=$(TF_DIR) validate

# Lint with tfsec (if installed)
.PHONY: lint
lint:
	which tfsec >/dev/null 2>&1 && tfsec $(TF_DIR) || echo "tfsec not installed, skipping"

# Plan
.PHONY: plan
plan: init validate
	$(TF) -chdir=$(TF_DIR) plan \
		-var="project_id=$(PROJECT_ID)" \
		-var="region=$(REGION)" \
		-out=tfplan

# Show plan
.PHONY: show
show:
	$(TF) -chdir=$(TF_DIR) show tfplan

# Apply (with optional auto-approve)
.PHONY: apply
apply: plan
	$(TF) -chdir=$(TF_DIR) apply $(AUTO_APPROVE) tfplan

# Full apply with auto-approve
.PHONY: apply-auto
apply-auto:
	$(MAKE) apply AUTO_APPROVE=-auto-approve

# Destroy
.PHONY: destroy
destroy: init
	$(TF) -chdir=$(TF_DIR) destroy \
		-var="project_id=$(PROJECT_ID)" \
		-var="region=$(REGION)"

# Output
.PHONY: output
output: init
	$(TF) -chdir=$(TF_DIR) output

# Show specific output
.PHONY: show-ips
show-ips: init
	@$(TF) -chdir=$(TF_DIR) output -json all_node_public_ips | jq -r '.[]' 2>/dev/null || \
	 $(TF) -chdir=$(TF_DIR) output all_node_public_ips

# Show mesh connection summary
.PHONY: summary
summary: init
	@$(TF) -chdir=$(TF_DIR) output mesh_connection_summary

# Import existing resource
.PHONY: import
import: init
	@read -p "Resource address: " addr; \
	 read -p "Resource ID: " id; \
	 $(TF) -chdir=$(TF_DIR) import $$addr $$id

# State list
.PHONY: state-list
state-list: init
	$(TF) -chdir=$(TF_DIR) state list

# Clean local files
.PHONY: clean
clean:
	rm -f tfplan tfplan.json
	rm -rf .terraform .terraform.lock.hcl

# Cost estimate with infracost (if installed)
.PHONY: cost
cost:
	which infracost >/dev/null 2>&1 && infracost breakdown --path=$(TF_DIR) || echo "infracost not installed, skipping"

# Full check: fmt + validate + lint
.PHONY: check
check: fmt validate lint

# Help
.PHONY: help
help:
	@echo "EVEZ Mesh Terraform Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  init          Initialize Terraform"
	@echo "  fmt           Format .tf files"
	@echo "  validate      Validate configuration"
	@echo "  lint          Run tfsec linter"
	@echo "  plan          Plan changes"
	@echo "  show          Show saved plan"
	@echo "  apply         Apply plan (manual approval)"
	@echo "  apply-auto    Apply with auto-approve"
	@echo "  destroy       Destroy all resources"
	@echo "  output        Show all outputs"
	@echo "  show-ips      Show all node IPs"
	@echo "  summary       Show mesh connection summary"
	@echo "  import        Import existing GCP resource"
	@echo "  state-list    List Terraform state resources"
	@echo "  cost          Estimate costs with infracost"
	@echo "  check         Run fmt + validate + lint"
	@echo "  clean         Remove local Terraform files"
