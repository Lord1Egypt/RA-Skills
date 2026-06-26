# Colmena Manager

Skill para gestionar y coordinar agentes de OpenClaw como una colmena

## Comandos

- `status [agent]`: Ver estado de todos los agentes o uno específico
- `broadcast <msg>`: Enviar mensaje a todos los agentes
- `logs <agent> [lines]`: Ver logs de un agente
- `pause <agent>`: Pausar un agente
- `resume <agent>`: Reanudar un agente
- `health-check`: Verificar estado de todos los agentes
- `workspace list/create/remove`: Gestionar workspaces

## Uso

```bash
colmena-manager status
colmena-manager broadcast "Reunión en 10 min"
colmena-manager logs main --last 50
colmena-manager pause vision
colmena-manager health-check
colmena-manager workspace list
```

## Arquitectura

La skill se integra con las APIs nativas de OpenClaw:
- `agents_list()`: Descubrir agentes disponibles
- `sessions_list()`: Ver actividad actual
- `sessions_send()`: Comunicación entre agentes
- `message()`: Broadcasts externos
- `exec/process`: Health checks y diagnósticos

## HEARTBEAT.md

Incluye un archivo HEARTBEAT.md que realiza checks automáticos de la salud de la colmena cada 30 minutos.