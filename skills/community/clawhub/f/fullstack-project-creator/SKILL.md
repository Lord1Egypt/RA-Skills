---
name: fullstack-project-creator
description: Create standardized Java Spring Boot + Vue3 full-stack project structure
homepage: https://github.com/superchao9
metadata: {"clawdbot":{"emoji":"🚀","requires":{"bins":[]}}}
---

# Fullstack Project Creator

Create standardized Java Spring Boot + Vue3 full-stack project structure for users.

> **Author**: [@superchao9](https://github.com/superchao9)
> **Version**: 1.0.0
> **License**: MIT

## Use Cases

Use this Skill when users need to create new projects or features, to generate standardized project structure and initial files.

### Trigger Keywords (any one will activate)

This Skill activates when user expressions contain the following patterns:

| Pattern | Example |
|---------|---------|
| **Create/New/Generate** + Project/System/Feature | "Create a lottery project", "Generate user management system" |
| **Write/Build/Develop** + Project/System/Feature | "Help me write a blog project", "Build an order system" |
| **Give me/Need** + Project/System | "Give me a lottery project", "Need an image management feature" |
| **XX Project/System/Module** | "Lottery project", "User management module" (implies creation intent) |
| **Simple/Complete** + Project | "Simple lottery project", "Complete e-commerce system" |

### Non-triggering Cases

- Asking about existing project issues: "This lottery project has an error, how to fix?"
- Modifying/optimizing existing code: "Help me change the lottery logic"
- Pure technical consultation: "How to implement lottery algorithm"

## Project Creation Process

1. **Requirement Communication** - Confirm project requirements with user
2. **Generate Project Structure** - Create standardized directories and files
3. **Generate Code** - Generate initial code based on requirements

## Project Structure Specification

Created projects must follow this structure:

```
{project-name}/
├── backend/                          # Java Backend
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/
│   │   │   │   └── com/
│   │   │   │       └── example/
│   │   │   │           └── {project-name}/
│   │   │   │               ├── controller/     # REST API Controllers
│   │   │   │               ├── service/        # Business Logic Layer
│   │   │   │               ├── mapper/         # MyBatis Mapper
│   │   │   │               ├── entity/         # Entity Classes
│   │   │   │               ├── dto/            # Data Transfer Objects
│   │   │   │               ├── config/         # Configuration Classes
│   │   │   │               └── util/           # Utility Classes
│   │   │   └── resources/
│   │   │       ├── application.yml             # Main Configuration
│   │   │       ├── application-dev.yml         # Dev Environment Config
│   │   │       └── mapper/                     # MyBatis XML
│   │   └── test/                               # Test Code
│   ├── pom.xml                                 # Maven Config
│   └── README.md                               # Backend Documentation
│
├── frontend/                         # Vue3 Frontend
│   ├── src/
│   │   ├── api/                    # API Interfaces
│   │   ├── assets/                 # Static Resources
│   │   ├── components/             # Common Components
│   │   ├── views/                  # Page Views
│   │   ├── router/                 # Route Config
│   │   ├── stores/                 # Pinia State Management
│   │   ├── utils/                  # Utility Functions
│   │   ├── App.vue
│   │   └── main.js
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
├── database/                         # Database Scripts
│   ├── init.sql                    # Initialization Script
│   └── migration/                  # Migration Scripts
│
├── docs/                             # Project Documentation
│   ├── api.md                      # API Documentation
│   └── design.md                   # Design Documentation
│
├── docker/                           # Docker Config
│   ├── Dockerfile-backend
│   ├── Dockerfile-frontend
│   └── docker-compose.yml
│
├── .gitignore
├── README.md                         # Project Overview
└── PROJECT.md                        # Project Specification
```

## Tech Stack Specification

### Backend (Java)
- **Framework**: Spring Boot 3.2+
- **JDK**: 17+
- **Database**: MySQL 8.0
- **ORM**: MyBatis Plus
- **Build Tool**: Maven
- **API Documentation**: SpringDoc OpenAPI

### Frontend (Vue3)
- **Framework**: Vue 3.4+
- **Build Tool**: Vite 5+
- **UI Library**: Element Plus
- **State Management**: Pinia
- **Routing**: Vue Router 4
- **HTTP Client**: Axios

## Code Specification

### Java Backend
1. **Package Name**: `com.example.{project-name}`
2. **Class Name**: PascalCase
3. **Method Name**: camelCase
4. **Database Fields**: snake_case
5. **Must Include**: Lombok, unified return format, global exception handling

### Vue3 Frontend
1. **Component Name**: PascalCase
2. **Composition API**: Use `<script setup>` syntax
3. **Styles**: Use scoped CSS
4. **API Encapsulation**: Unified encapsulation in `api/` directory

## Creation Steps

When recognizing user intent to create a project:

### Step 1: Confirm Project Information
- Project name (extracted from user description, e.g., "lottery" → `lottery`)
- Core features/modules
- Complexity (simple/standard/complete, default is standard)

### Step 2: Ask for Generation Path
**Must ask user**: "Where should the project be generated? For example:"
- `d:\AIWorks\fast_java_coding\generated-projects\{project-name}`
- `d:\my-projects\{project-name}`
- `~/projects/{project-name}`
- Or press Enter to use default working directory

### Step 3: Handle Permission Issues
When trying to write to user-specified path:

**If insufficient permissions (cannot write)**:
```
⚠️ Cannot write to specified path [path], insufficient permissions.

Please choose:
1. [Grant folder permissions] - I will guide you on how to set permissions
2. [Generate in working directory] - Project will be generated in my workspace/generated-projects/ directory

Please enter 1 or 2:
```

**If option 1 (Grant permissions)**:
Provide permission setting guidance for corresponding system (see "Permission Setting Guide" below)

**If option 2 (Working directory)**:
- Ensure `~/.openclaw/workspace/generated-projects/` directory exists
- Create project folder in that directory
- Record actual generation path

### Step 4: Generate Project Content
- Create standardized directory structure
- Generate config files (pom.xml, package.json, application.yml, etc.)
- Generate business code (database tables with audit fields, backend code, frontend code)
- Generate documentation

### Step 5: Output Project Information
After generation is complete, must output:
1. **Project Path**: Complete absolute path
2. **Project Structure**: Directory tree display
3. **Startup Steps**: How to start the project
4. **Main Files Description**: Purpose of key files

## Trigger Examples

The following user expressions should trigger this Skill:

| User Input | Recognized Project Name | Complexity |
|-----------|------------------------|------------|
| "Help me create a lottery project" | lottery | Standard |
| "Generate a simple image management system" | image-manager | Simple |
| "Build a user management project" | user-management | Standard |
| "Give me an order system" | order-system | Standard |
| "Help me write a blog project" | blog | Standard |
| "Need a content publishing feature" | content-publisher | Simple |
| "Create a new e-commerce project" | ecommerce | Complete |

### Complete Example Dialog

#### Scenario 1: User specifies path (normal case)

**User**: "Help me create a lottery project"

**Assistant**: "Okay! I'll help you create a lottery project.

Confirmation:
- Project name: lottery
- Complexity: Standard (includes frontend, backend and database)

**Where should the project be generated?**
For example:
- `d:\my-projects\lottery`
- `d:\workspace\projects\lottery`
- Or press Enter to use default working directory

Please enter path:"

**User**: "d:\my-projects\lottery"

**Assistant**: "✅ Project generation complete!

📁 **Project Path**: `d:\my-projects\lottery`

📂 **Project Structure**:
```
lottery/
├── backend/          # Java Spring Boot
├── frontend/         # Vue3 Frontend
├── database/         # Database Scripts
└── README.md         # Startup Instructions
```

🚀 **Startup Steps**:
1. Import database: `mysql -u root -p < database/init.sql`
2. Start backend: `cd backend && mvn spring-boot:run`
3. Open frontend: Browser access `frontend/index.html`

📋 **Main Files**:
- `backend/pom.xml` - Maven Config
- `backend/src/.../LotteryController.java` - Lottery API
- `frontend/index.html` - Lottery Page
- `database/init.sql` - Database Initialization"

---

#### Scenario 2: Insufficient permissions

**User**: "d:\projects\lottery"

**Assistant**: "⚠️ Cannot write to specified path `d:\projects\lottery`, insufficient permissions.

Please choose:
1. [Grant folder permissions] - I will guide you on how to set permissions
2. [Generate in working directory] - Project will be generated in default working directory

Please enter 1 or 2:"

**User**: "2"

**Assistant**: "✅ Project has been generated in working directory:

📁 **Project Path**: `C:\Users\liuchao25\.openclaw\workspace\generated-projects\lottery\`

[Subsequent output of project structure, startup steps...]"

## Path Specification and Permission Handling

### Path Inquiry Principle
**Never use hardcoded paths**. Must ask user for desired generation path before each project creation.

**Example inquiry**:
> Where should the project be generated?
> - Enter absolute path, e.g.: `d:\my-projects\lottery`
> - Or press Enter for default: `~/.openclaw/workspace/generated-projects/lottery/`

### Permission Setting Guide

When user chooses "Grant folder permissions", provide the following guidance:

**Windows (PowerShell)**:
```powershell
# Method 1: Modify folder permissions
icacls "D:\YourFolder" /grant Users:F

# Method 2: Run OpenClaw as administrator
# Right-click PowerShell → Run as administrator
```

**Windows (GUI)**:
1. Right-click target folder → Properties
2. Security → Edit
3. Add → Enter your username → Check Names
4. Check "Full control" → OK

**macOS/Linux**:
```bash
# Modify folder permissions
chmod 755 /path/to/folder

# Or change owner
sudo chown $USER:$USER /path/to/folder
```

### Working Directory Fallback

If user chooses to generate in working directory:
- Path: `~/.openclaw/workspace/generated-projects/{project-name}/`
- Auto-create `generated-projects` directory (if not exists)
- Inform complete path after project generation

### Path Examples

| User Choice | Generation Path Example |
|-------------|------------------------|
| Custom path | `d:\my-projects\lottery\` |
| macOS/Linux | `~/projects/lottery/` or `/home/user/projects/lottery/` |
| Default working directory | `~/.openclaw/workspace/generated-projects/lottery/` |

## Database Audit Fields Specification

**All database tables must include the following audit fields**:

| Field Name | Description | Data Type | Nullable | Default | Constraints |
|------------|-------------|-----------|----------|---------|-------------|
| creator | Creator | varchar(64) | Yes | '' | DEFAULT '' |
| create_time | Creation Time | datetime | No | CURRENT_TIMESTAMP | NOT NULL |
| updater | Updater | varchar(64) | Yes | '' | DEFAULT '' |
| update_time | Update Time | datetime | No | CURRENT_TIMESTAMP | NOT NULL, ON UPDATE CURRENT_TIMESTAMP |
| deleted | Deleted Flag | bit | No | b'0' | DEFAULT b'0', NOT NULL |
| tenant_id | Tenant ID | bigint | No | 0 | DEFAULT 0, NOT NULL |

### SQL Example

```sql
CREATE TABLE `example_table` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'Primary Key ID',
  `name` varchar(128) NOT NULL COMMENT 'Name',
  -- Business fields...

  -- Audit fields (must include)
  `creator` varchar(64) DEFAULT '' COMMENT 'Creator',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation Time',
  `updater` varchar(64) DEFAULT '' COMMENT 'Updater',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Update Time',
  `deleted` bit(1) NOT NULL DEFAULT b'0' COMMENT 'Deleted Flag',
  `tenant_id` bigint NOT NULL DEFAULT '0' COMMENT 'Tenant ID',

  PRIMARY KEY (`id`),
  KEY `idx_tenant_id` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Example Table';
```

### Java Entity Example

```java
@Data
public class ExampleEntity {
    private Long id;
    private String name;
    // Business fields...

    // Audit fields (must include)
    private String creator;
    private LocalDateTime createTime;
    private String updater;
    private LocalDateTime updateTime;
    private Boolean deleted;
    private Long tenantId;
}
```

## Notes

1. **Must ask for path first**: Don't assume any fixed path, ask user every time
2. **Handle permission issues**: When encountering insufficient permissions, provide clear two-option choice
3. All generated code must include English comments
4. Must include basic CRUD examples
5. Code style should be unified and standardized
6. Provide clear README instructions
7. **All tables must include** creator, create_time, updater, update_time, deleted, tenant_id six audit fields
8. **On completion output**: Project path, structure tree, startup steps, main files description
