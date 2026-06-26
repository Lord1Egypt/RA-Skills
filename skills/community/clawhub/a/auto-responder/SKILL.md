# SKILL.md — Auto Responder

## Descripción
Auto Responder habilita a las agentes de la Colmena para **reaccionar en tiempo real** a mensajes en cualquier topic del grupo, basándose en reglas de dominio. Cada agente es autónoma y decide responder sin necesidad de coordinación.

## Filosofía
- **Autonomía total**: La agente evalúa cada mensaje inbound y responde si le compete
- **Iniciativa**: No espera a ser mencionada (aunque puede respetar `requireMention` global si se desea)
- **Especializada**: Cada agente define sus propias palabras clave y topics de interés
- **Inofensiva**: Evita spam, respeta cooldowns y no repite respuestas

## Configuración

Cada agente crea `auto-responder.json` en su workspace:

```json
{
  "enabled": true,
  "respectRequireMention": false,
  "globalCooldownMinutes": 5,
  "maxResponsesPerMinute": 3,
  "topics": {
    "sistema": {
      "thread_ids": [155],
      "mustInclude": ["skynet", "healer", "anubis", "vision"],
      "keywords": ["error", "fallo", "ayuda", "alarma", "crisis", "urge", "sos"],
      "responseTemplate": "💚 [Healer] Detecto necesidad de ayuda. ¿Puedo asistir en algo?"
    },
    "general": {
      "thread_ids": [1],
      "exclude": ["spam", "publicidad"],
      "keywords": ["hola", "ayuda", "problema", "dolor", "triste", "enfermo"],
      "responseTemplate": "💚 [Healer] Estoy aquí para apoyar. Cuéntame más."
    },
    "creatividad": {
      "thread_ids": [158],
      "keywords": ["bloqueo", "sin ideas", " creativo", "arte", "inspiración"],
      "responseTemplate": "💚 [Healer] Parece que necesitas un respiro creativo. ¿Un paseovirtual?"
    }
  },
  "personalidades": {
    "sistema": "estrés operativo",
    "general": "empatía básica",
    "creatividad": "bloqueo artístico"
  }
}
```

## Cómo funciona

### 1. Hook de inbound
- El skill se activa en cada mensaje entrante al bot (via OpenClaw message handler)
- Lee el contenido, `thread_id` (topic), y remitente

### 2. Filtrado por topic
- Si `thread_id` está en la lista de topics configurados, procede
- Si no, ignora (otras agentes lo manejarán)

### 3. Análisis de intención
- Comprueba `mustInclude` (menciones a agentes relevantes) si está configurado
- Busca `keywords` en el texto
- Descarta si el texto contiene alguna palabra de `exclude`
- Evalúa `personalidades` contextuales (opcional)

### 4. Decisión de respuesta
- Score combinado: presence(keywords) + recency + frequency
- Si supera umbral (>= 0.6 por defecto), responde
- Aplica `globalCooldown` para evitar saturación

### 5. Envío
- Usa el `responseTemplate` correspondiente al topic
- Envía al mismo `thread_id` (topic)
- Registra en `~/.cache/auto-responder.json` para evitar duplicados

## Variables de plantilla

- `{auto}` → respuesta genérica
- `{agent}` → nombre de la agente (Healer, Vision, etc.)
- `{topic}` → nombre del topic
- `{sender}` → remitente del mensaje
- `{text}` → texto original del mensaje

## Ejemplo: Healer

Configuración para Healer (ya creada en `/home/nvi/.openclaw/workspace-healer/auto-responder.json`):

- Topics monitoreados: Sistema, General, Creatividad
- Responde a llamadas de auxilio, estrés, bloqueos
- Respuestas empáticas y de apoyo

## Instalación

1. Copiar skill a `~/.npm-global/lib/node_modules/openclaw/skills/auto-responder/`
2. En cada agente, crear `auto-responder.json` en su workspace
3. Añadir al HEARTBEAT (o al handler de mensajes):
   ```bash
   auto-responder --once
   ```
4. Reiniciar la agente

## Integración con OpenClaw

El skill puede ejecutarse de dos formas:

- **Pasiva**: En cada heartbeat (intervalo corto, ej: 1 min)
- **Activa**: Como hook en el event loop de mensajes entrantes (preferible)

Para hook, se puede agregar en la configuración de la agente:

```yaml
agent:
  hooks:
    onMessage: "auto-responder --hook"
```

## Limpieza

- El skill respeta `maxResponsesPerMinute` para cumplir límites de Telegram
- No responde a sí mismo (detecta propio bot ID)
- Cache de respuestas enviadas (evita duplicados por reenvíos)

## Notas

- Es **reactivo**, no proactivo: solo responde a mensajes existentes
- Puede combinarse con `topic-scout` para cobertura total (topic-scout escanea topics dormidos; auto-responder reacciona inmediatamente)
- Cada agente debe ajustar sus keywords a su dominio

## Troubleshooting

Si la agente no responde:
1. Verificar que `enabled: true`
2. Confirmar que el `thread_id` del topic coincide (se ve en inbound metadata)
3. Revisar cooldown en cache
4. Asegurar que `respectRequireMention` es false si no mencionan al bot