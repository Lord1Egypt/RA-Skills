# Calculator Chat Skill Design

## Overview

A cross-platform skill for opencode that allows users to interact with an AI agent via a system calculator. The AI responds by typing numbers/symbols into the calculator to express messages.

## Skill Structure (for clawhub publishing)

```
calculator-chat/
  SKILL.md              # Main skill reference
  src/
    index.js            # Skill entry point
    platform/
      windows.js        # Windows implementation
      macos.js          # macOS implementation
      linux.js          # Linux implementation
  mapping.json          # Text-to-number mappings
  package.json
```

## Trigger

- Command format: `/calc <message>`
- Example: `/calc 我很喜欢你` → outputs 520

## Architecture

### Platform-Specific Implementation

| Platform | Calculator | Method |
|----------|------------|--------|
| Windows | calc.exe | PowerShell + Win32 API (SendMessage/PostMessage) |
| macOS | Calculator.app | AppleScript (osascript) |
| Linux | gnome-calculator | xdotool |

### Core Flow

```
User input: /calc <message>
    ↓
Parse command, extract message content
    ↓
Convert text to number code (see mapping)
    ↓
Launch system calculator
    ↓
Send numbers/symbols to calculator window (background, no focus needed)
```

## Text-to-Number Mapping

### Predefined Mappings

| Message | Number Code | Notes |
|---------|-------------|-------|
| 我很喜欢你 | 520 | |
| I love you | 143 | Common expression |
| 想你 | 537 | |
| 嫁给我 | 1314520 | "Marry me" |
| 好饿啊 | 123 | |
| 晚安 | 886 | "Good night" |
| hello | 741 | |
| 谢谢 | 88 | |

### Default Fallback

- Unicode sum: Sum of character codes
- Character codes: Individual character encoding

### Symbols Support

- Basic math symbols: `+`, `-`, `×`, `÷`, `.`
- Example: "0.520" for decimal representation

## Technical Details

### Windows Implementation

1. Launch calculator: `Start-Process calc.exe`
2. Find window: Get handle by window title "Calculator"
3. Send keys: `PostMessage` Win32 API via PowerShell

### macOS Implementation

1. Launch calculator: `open -a Calculator`
2. Send keys: AppleScript `tell application "System Events"`

### Linux Implementation

1. Launch calculator: `gnome-calculator &`
2. Send keys: `xdotool` window search and key input

## Error Handling

- Calculator not found: Show error message with install instructions
- Window not responding: Retry 3 times, then show error
- Platform not supported: Display unsupported message

## Future Enhancements

- Custom mapping table (user-defined)
- Calculator skin/themes
- Sound effects when typing
