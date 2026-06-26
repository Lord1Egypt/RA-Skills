# cae_skill

Windows local CAE control skill.

Supported apps:
- abaqus
- ansys
- ansa
- hyperworks

Capabilities:
- launch_app
- open_file_in_app
- is_app_running
- close_app
- get_active_app
- get_running_apps
- detect_app_path
- set_app_path

Notes:
- does not scan the whole computer
- does not read the Windows registry
- only checks saved paths and predefined common paths
- some software launch commands may need local adjustment depending on version and installation style