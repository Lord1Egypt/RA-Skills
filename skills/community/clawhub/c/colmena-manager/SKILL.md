# 🐺 Colmena Manager

Skill para gestionar y coordinar agentes de OpenClaw como una colmena.

## 📋 Descripción

Colmena Manager permite monitorear, comunicar y gestionar todos los agentes de la colmena desde una única interfaz. Ideal para mantener el control de múltiples instancias de OpenClaw corriendo en diferentes workspaces o contextos.

## 🔧 Comandos CLI

### `status [agent]`

Muestra el estado de todos los agentes o uno específico.

**Opciones:**
- `agent` (opcional): ID del agente específico a consultar

**Ejemplo:**
```bash
colmena-manager status
colmena-manager status main
```

### `broadcast <msg>`

Envía un mensaje a todos los agentes de la colmena.

**Ejemplo:**
```bash
colmena-manager broadcast "Reunión de sincronización en 10 minutos"
```

### `logs <agent> [lines]`

Muestra las últimas líneas del log de un agente.

**Opciones:**
- `agent` (requerido): ID del agente
- `lines` (opcional, default: 50): Número de líneas a mostrar

**Ejemplo:**
```bash
colmena-manager logs vision --last 100
colmena-manager logs healer 25
```

### `pause <agent>`

Pausa temporalmente un agente.

**Ejemplo:**
```bash
colmena-manager pause nemotron
```

### `resume <agent>`

Reanuda un agente previamente pausado.

**Ejemplo:**
```bash
colmena-manager resume vision
```

### `health-check`

Realiza una verificación completa del estado de salud de todos los agentes (procesos, sesiones, memoria).

**Ejemplo:**
```bash
colmena-manager health-check
```

### `workspace`

Comandos para gestionar workspaces de agentes:

- `workspace list`: Lista todos los workspaces disponibles
- `workspace create <name>`: Crea un nuevo workspace
- `workspace remove <name>`: Elimina un workspace

**Ejemplo:**
```bash
colmena-manager workspace list
colmena-manager workspace create project-x
colmena-manager workspace remove old-workspace
```

## 🔌 Integración con OpenClaw APIs

La skill utiliza las siguientes APIs nativas:

- `agents_list()`: Descubre todos los agentes registrados
- `sessions_list()`: Consulta sesiones activas por agente
- `sessions_send()`: Envía comandos/mensajes a agentes específicos
- `message()`: Para broadcasts externos a través de canales
- `exec` / `process`: Para health checks y diagnósticos del sistema

## 🔄 HEARTBEAT.md

La skill incluye un archivo `HEARTBEAT.md` que se ejecuta automáticamente cada 30 minutos para:

- Verificar el estado de todos los agentes
- Detectar agentes caídos
- Monitorear uso de memoria
- Generar reportes de salud

Esto permite mantener la colmena vigilada sin intervención manual.

## 📦 Instalación

```bash
# Instalar desde clawhub
clawhub install colmena-manager

# O desde el directorio fuente
npm install /path/to/colmena-manager
```

## 🚀 Publicación

Para publicar una nueva versión en clawhub.com:

```bash
cd colmena-manager
clawhub publish
```

## 📁 Estructura del proyecto

```
colmena-manager/
├── package.json
├── claws.json          # Manifiesto para clawhub
├── SKILL.md            # Documentación (este archivo)
├── README.md           # Detalles técnicos
├── src/
│   └── index.js        # Implementación principal
└── HEARTBEAT.md        # Scripts automáticos de monitoreo
```

## 🔄 Compatibilidad

- OpenClaw >= 1.0.0
- Node.js >= 18
- Linux/macOS/Windows

## 📝 Ejemplos de uso

### 1. Monitorizar toda la colmena
```bash
colmena-manager status
```

### 2. Ver logs de un agente
```bash
colmena-manager logs main 100
```

### 3. Broadcast urgente
```bash
colmena-manager broadcast "SISTEMA EN MANTENIMIENTO - PAUSA INMINENTE"
```

### 4. Health check programado
```bash
# Agregar a cron cada 30min
*/30 * * * * colmena-manager health-check >> /var/log/colmena-health.log
```

## ⚠️ Consideraciones

- Los agentes deben estar corriendo y registrados para que los comandos funcionen
- `pause` y `resume` envían señales que cada agente debe manejar individualmente
- Los workspaces son directorios locales bajo `/home/nvi/.openclaw/workspace-*`
- Asegurar permisos de ejecución en el script principal