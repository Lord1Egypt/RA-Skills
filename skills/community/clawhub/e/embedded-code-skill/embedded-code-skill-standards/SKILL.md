---
name: embed-code-standards
description: Embedded C coding standards reference. Naming conventions, type standards, error handling, struct/enum patterns, comment rules.
---

# Coding Standards

## Naming

| Element | Convention | Example |
|---------|------------|---------|
| Variables | snake_case | `sensor_value` |
| Globals | g_snake_case | `g_system_ticks` |
| Constants | SCREAMING_SNAKE | `MAX_BUFFER_SIZE` |
| Macros | SCREAMING_SNAKE | `GPIO_MODE_INPUT` |
| Functions | camelCase | `initUart()` |
| Struct types | snake_case_t | `uart_config_t` |
| Enum types | snake_case_t | `gpio_state_t` |
| Enum values | PREFIXED_SNAKE | `GPIO_STATE_LOW` |
| Pointers | p_snake_case | `p_rx_buffer` |

## Types

Use only stdint.h types:

```
uint8_t  → byte, GPIO
uint16_t → 16-bit registers
uint32_t → 32-bit registers
int32_t  → signed values
bool     → flags
```

**NEVER**: int, char, long (unless necessary)

## Includes (Required)

```c
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
```

## Error Handling

```c
typedef enum {
    EmbedCode_Ok = 0,
    EmbedCode_ErrNullPtr = -1,
    EmbedCode_ErrInvalidArg = -2,
    EmbedCode_ErrTimeout = -3,
    EmbedCode_ErrBusy = -4
} embed_code_status_t;

#define VALIDATE_NOT_NULL(ptr) \
    do { if ((ptr) == NULL) return EmbedCode_ErrNullPtr; } while(0)
```

Every public function:
- Returns `embed_code_status_t`
- Validates NULL pointers
- Returns specific error codes

## Struct Patterns

```c
// Config - const after init
typedef struct {
    uint32_t base_address;
    uint8_t  priority;
} peripheral_config_t;

// Handle - runtime state
typedef struct {
    bool                initialized;
    peripheral_config_t config;
} peripheral_handle_t;

// State enum
typedef enum {
    STATE_IDLE = 0,
    STATE_RUNNING,
    STATE_ERROR
} state_t;
```

## No Dynamic Allocation

**PROHIBITED**: malloc, free, calloc, realloc, new, delete, VLAs

**ALWAYS**: Fixed-size buffers

```c
#define BUFFER_SIZE 256U
uint8_t buffer[BUFFER_SIZE];
```

## Comments

**语言: 优先使用中文**

```c
// ✅ 正确 - 使用中文注释,解释 WHY
config |= (1U << 3);  /* 低电平有效 */

// ❌ 错误 - 使用英文注释
config |= (1U << 3);  /* Active-low enable */

// ❌ 错误 - 解释代码本身已清楚表达的内容
i++;  /* i 自增 */
```

**注释原则:**
- **中文优先**: 便于团队阅读和维护
- **解释 WHY**: 说明原因和意图,而非描述代码在做什么
- **代码自说明**: 如果代码本身已清楚表达含义,无需注释

## Quality Checklist

- [ ] stdint.h types only
- [ ] Naming correct
- [ ] Public functions return status
- [ ] NULL validation
- [ ] No magic numbers
- [ ] Comments explain WHY
- [ ] No malloc/free
