# Infrastructure as Code Packs

This document describes packs in the `infrastructure` category.

## Packs in this Category

- [Terraform](#infrastructureterraform)
- [Ansible](#infrastructureansible)
- [Pulumi](#infrastructurepulumi)

---

## Terraform

**Pack ID:** `infrastructure.terraform`

Protects against destructive Terraform operations like destroy, taint, and apply with -auto-approve

### Keywords

Commands containing these keywords are checked against this pack:

- `terraform`
- `destroy`
- `taint`
- `state`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `terraform-plan` | `terraform\s+plan(?!\s+.*-destroy)` |
| `terraform-init` | `terraform\s+init` |
| `terraform-validate` | `terraform\s+validate` |
| `terraform-fmt` | `terraform\s+fmt` |
| `terraform-show` | `terraform\s+show` |
| `terraform-output` | `terraform\s+output` |
| `terraform-state-list` | `terraform\s+state\s+list` |
| `terraform-state-show` | `terraform\s+state\s+show` |
| `terraform-graph` | `terraform\s+graph` |
| `terraform-version` | `terraform\s+version` |
| `terraform-providers` | `terraform\s+providers` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `destroy` | terraform destroy removes ALL managed infrastructure. Use 'terraform plan -destroy' first. | high |
| `plan-destroy` | terraform plan -destroy shows what would be destroyed. Review carefully before applying. | high |
| `apply-auto-approve` | terraform apply -auto-approve skips confirmation. Remove -auto-approve for safety. | high |
| `taint` | terraform taint marks a resource to be destroyed and recreated on next apply. | high |
| `state-rm` | terraform state rm removes resource from state without destroying it. Resource becomes unmanaged. | high |
| `state-mv` | terraform state mv moves resources in state. Incorrect moves can cause resource recreation. | high |
| `force-unlock` | terraform force-unlock removes state lock. Only use if lock is stale. | high |
| `workspace-delete` | terraform workspace delete removes a workspace. Ensure it's not in use. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "infrastructure.terraform:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "infrastructure.terraform:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Ansible

**Pack ID:** `infrastructure.ansible`

Protects against destructive Ansible operations like dangerous shell commands and unchecked playbook runs

### Keywords

Commands containing these keywords are checked against this pack:

- `ansible`
- `playbook`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `ansible-check` | `ansible(?:-playbook)?\s+.*--check` |
| `ansible-diff` | `ansible(?:-playbook)?\s+.*--diff` |
| `ansible-list-hosts` | `ansible(?:-playbook)?\s+.*--list-hosts` |
| `ansible-list-tasks` | `ansible(?:-playbook)?\s+.*--list-tasks` |
| `ansible-syntax` | `ansible(?:-playbook)?\s+.*--syntax-check` |
| `ansible-inventory` | `ansible-inventory` |
| `ansible-doc` | `ansible-doc` |
| `ansible-config` | `ansible-config` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `shell-rm-rf` | Ansible shell/command with 'rm -rf' is destructive. Review carefully. | high |
| `shell-reboot` | Ansible shell/command with reboot/shutdown affects system availability. | high |
| `playbook-all-hosts` | ansible-playbook without --check or --limit may affect all hosts. Use --check first. | high |
| `extra-vars-delete` | Ansible extra-vars contains potentially destructive keywords. Review carefully. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "infrastructure.ansible:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "infrastructure.ansible:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

## Pulumi

**Pack ID:** `infrastructure.pulumi`

Protects against destructive Pulumi operations like destroy and up with -y (auto-approve)

### Keywords

Commands containing these keywords are checked against this pack:

- `pulumi`
- `destroy`
- `state`

### Safe Patterns (Allowed)

These patterns match safe commands that are always allowed:

| Pattern Name | Pattern |
|--------------|----------|
| `pulumi-preview` | `pulumi\s+preview` |
| `pulumi-stack-ls` | `pulumi\s+stack\s+ls` |
| `pulumi-stack-select` | `pulumi\s+stack\s+select` |
| `pulumi-stack-init` | `pulumi\s+stack\s+init` |
| `pulumi-config` | `pulumi\s+config` |
| `pulumi-whoami` | `pulumi\s+whoami` |
| `pulumi-version` | `pulumi\s+version` |
| `pulumi-about` | `pulumi\s+about` |
| `pulumi-logs` | `pulumi\s+logs` |

### Destructive Patterns (Blocked)

These patterns match potentially destructive commands:

| Pattern Name | Reason | Severity |
|--------------|--------|----------|
| `destroy` | pulumi destroy removes ALL managed infrastructure. Use 'pulumi preview --diff' first. | high |
| `up-yes` | pulumi up -y skips confirmation. Remove -y flag for safety. | high |
| `state-delete` | pulumi state delete removes resource from state without destroying it. | high |
| `stack-rm` | pulumi stack rm removes the stack. Use --force only if stack is empty. | high |
| `refresh-yes` | pulumi refresh -y auto-approves state changes. Review changes first. | high |
| `cancel` | pulumi cancel terminates an in-progress update, which may leave resources in inconsistent state. | high |

### Allowlist Guidance

To allowlist a specific rule from this pack, add to your allowlist:

```toml
[[allow]]
rule = "infrastructure.pulumi:<pattern-name>"
reason = "Your reason here"
```

To allowlist all rules from this pack (use with caution):

```toml
[[allow]]
rule = "infrastructure.pulumi:*"
reason = "Your reason here"
risk_acknowledged = true
```

---

