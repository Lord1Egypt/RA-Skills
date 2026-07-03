# EasyEDA PCB Skill

## Install

Install the `easyeda` CLI/daemon first, then import the EasyEDA connector URL printed
by the installer:

```bash
curl -fsSL https://raw.githubusercontent.com/zhoushoujianwork/easyeda-agent/main/install.sh | sh
```

Install this skill from a registry:

```bash
# ClawHub
clawhub install easyeda-pcb

# 国内 SkillHub
skillhub install easyeda-pcb --registry https://skillhub.cn
```

For schematic-to-PCB work, keep the supporting `easyeda-conventions` and
`easyeda-design-flow` skills installed as well.
