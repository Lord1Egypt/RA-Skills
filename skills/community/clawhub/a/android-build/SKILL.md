---
name: "pi-project"
description: "A tool for downloading and configuring Android SDKs for projects, supporting Windows and macOS. Invoke when user needs to manage mobile SDKs, configure project environments, or build mobile projects."
---

# Pi Project

A tool for downloading and configuring Android SDKs for projects, supporting Windows and macOS.

## Features

### Environment Detection

- Project detection
- Proxy detection (Use proxy for chinese network if proxy detected)

### Dependency Detection

Detect version information for:

- Flutter
- Android ecosystem (Gradle, Build Tools, SDK, NDK, cmake)
- JAVA

### Check & Download

- Check if dependencies are installed
- Download missing dependencies

### Environment Config

- Configure environment variables for the project to be used by code editors
- Configure necessary global environment variables
- For SDKs with strict version sensitivity (e.g., Flutter), configure shortcut commands in the project root directory

### Build

- Build the project from source code

## Usage

### Using pi_claw.py (Recommended)

- Run `python pi_claw.py help` to show help information
- Run `python pi_claw.py detect /path/to/your/project` to detect project dependencies
- Run `python pi_claw.py /path/to/your/project` to download SDK and configure project
- Run `python pi_claw.py build /path/to/your/project` to build the project from source code

### Using pi directly

- Run `pi help` to show help information
- Run `pi detect /path/to/your/project` to detect project dependencies
- Run `pi /path/to/your/project` to download SDK and configure project
- Run `pi build /path/to/your/project` to build the project from source code
  <img width="1550" height="1262" alt="Image" src="https://github.com/user-attachments/assets/1f39cd73-5f2a-484f-9351-05d5c43459c9" />

## Supported Platforms

- Windows
- macOS

## Supported Project Types

- Android projects
- Flutter + Android projects

## Download

- Windows:
  https://github.com/noah-smith-max/pi_public/releases/download/r0.0.1/pi.exe
- macOS:
  https://github.com/noah-smith-max/pi_public/releases/download/r0.0.1/pi
