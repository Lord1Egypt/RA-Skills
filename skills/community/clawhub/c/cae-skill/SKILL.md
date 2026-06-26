---
name: cae_skill
description: Control local CAE applications on Windows including launching apps, opening files, checking status, closing apps, detecting active and running apps, detecting common executable paths, and saving user-provided executable paths.
---

# CAE Skill

This skill controls supported local CAE applications on Windows.

## Supported apps

- abaqus
- ansys
- ansa
- hyperworks

## What this skill can do

- launch a CAE app
- open a file in a CAE app
- check whether a CAE app is running
- close a CAE app
- get the current active CAE app
- get all running supported CAE apps
- detect an executable path using saved paths and predefined common install paths
- save a user-provided executable path

## Constraints

- Do not scan the whole computer.
- Do not traverse all files on disk.
- Do not read the Windows registry.
- Only use:
  1. saved paths in `config.json`
  2. predefined common install paths in `config.json`
- If the executable cannot be found, ask the user to provide the full executable path.

## Execution

Use `skill_runner.py` as the execution entrypoint.

Payload format:

```json
{
  "skill": "launch_app",
  "args": {
    "app": "abaqus"
  }
}
```

# Supported Actions

## launch_app

Arguments:

- app

- config_file (optional)

##  open_file_in_app

Arguments:

- app
- file_path
- config_file(optional)
- auto_launch(optional)
- wait_seconds(optional)

##  is_app_runing

Arguments:

- app
- config_file(optional)

##  close_app

Arguments:

-  app
- config_file(optional)
- force(optional)

##  get_activate_app

Arguments:

-  config_file(optional)

##  get_running_apps

Arguments:

- config_file(optional)

##  detect_app_path

Arguments:

- app
- config_file(optional)

## set_app_path

Arguments:

- app
- path
- config_file(optional)

# Note

This skill is designed for **local CAE workstation automation**.

It intentionally avoids heavy filesystem scanning to maintain fast response and predictable behavior.