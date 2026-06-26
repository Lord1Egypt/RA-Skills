---
name: corelocationcli
description: Get the physical location of your macOS device and print it to stdout.
metadata: {"clawdbot":{"emoji":"📍","requires":{"bins":["swift"],"os":"macOS"}}}
---

# CoreLocationCLI

Gets the physical location of your device and prints it to standard output. Kill it with CTRL-C.

**Note:** Make sure Wi-Fi is turned on, otherwise you will see `kCLErrorDomain error 0`.

## Usage

```bash
CoreLocationCLI --help
CoreLocationCLI --version
CoreLocationCLI [--watch] [--verbose] [--format FORMAT]
CoreLocationCLI [--watch] [--verbose] --json
```

| Switch            | Description                                     |
| ----------------- | ----------------------------------------------- |
| `-h`, `--help`    | Display help message and exit                   |
| `--version`       | Display the program version                     |
| `-w`, `--watch`   | Continually print location updates              |
| `-v`, `--verbose` | Show debugging output                           |
| `-f`, `--format`  | Print a string with the specified substitutions  |
| `-j`, `--json`    | Print a JSON object with all available information |

## Format Specifiers

Location: `%latitude` `%longitude` `%altitude` `%direction` `%speed` `%h_accuracy` `%v_accuracy` `%time`

Reverse geocoding: `%address` `%name` `%isoCountryCode` `%country` `%postalCode` `%administrativeArea` `%subAdministrativeArea` `%locality` `%subLocality` `%thoroughfare` `%subThoroughfare` `%region` `%timeZone` `%time_local`

Default format: `%latitude %longitude`

## Examples

```bash
CoreLocationCLI
# 50.943829 6.941043

CoreLocationCLI --format "%latitude %longitude\n%address"
# 50.943829 6.941043
# Kaiser-Wilhelm-Ring 21
#  Cologne North Rhine-Westphalia 50672
#  Germany

CoreLocationCLI --json
# {"latitude":"40.141196","longitude":"-75.034815","altitude":"92.00",...}
```

## Installation

```bash
brew install cask corelocationcli
```

## Gatekeeper

First run may be blocked by macOS Gatekeeper. Go to System Settings → Privacy & Security → Security to approve.
