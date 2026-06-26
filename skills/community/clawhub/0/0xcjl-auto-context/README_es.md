# auto-context

> Verificador de higiene de contexto para agentes de IA

[English](./README.md) · [中文](./README_zh.md) · [日本語](./README_ja.md)

## Descripción General

**auto-context** es un verificador inteligente de salud de contexto diseñado para asistentes de codificación IA. Analiza los niveles de contaminación del contexto de la sesión (conversaciones largas, deriva de temas, acumulación de ruido) y recomienda acciones: continue, /fork, /btw, o nueva sesión.

## ¿Por qué este skill?

La gestión de contexto es crítica para los agentes IA. A medida que las conversaciones grow longer, la contaminación del contexto (deriva de temas, acumulación de ruido, llamadas redundantes de herramientas) degrada la calidad de las respuestas. Las soluciones tradicionales como compresión o reset de sesión son reactivas—AutoContext proporciona **recomendaciones proactivas** antes de que ocurran los problemas.

### Base de Investigación
- Papers ArXiv sobre gestión de ventana de contexto
- Teoría de carga cognitiva de psicología
- Limitaciones de memoria de trabajo en interacción humano-IA

## Características

### Evaluación Multidimensional (5 Dimensiones)

| Dimensión | Métrica | Umbral | Peso |
|-----------|---------|--------|------|
| Longitud de Conversación | Turnos consecutivos | >30 turnos | 20% |
| Coherencia de Tema | Conteo de deriva | 2+ derivas | 25% |
| Densidad de Información | Palabras/turno | <50 | 15% |
| Eficiencia de Herramientas | Salida válida | <10% | 20% |
| Conteo de Compresión | Compresiones | 2+ | 20% |

### Niveles de Salud

- 🟢 **HEALTHY** (80-100): Continuar tema actual
- 🟡 **NOISY** (60-79): Continuar pero monitorear eficiencia
- 🔴 **POLLUTED** (40-59): Recomendar /fork o /btw
- ⛔ **CRITICAL** (<40): Recomendar nueva sesión

### Modos de Activación Dual

1. **Manual**: `/auto-context` para reporte completo de salud
2. **Auto**: Activación en capa de respuesta cuando se detectan señales

### Señales de Activación Automática

- 20+ turnos consecutivos sin progreso
- Deriva de tema (tema actual no relacionado con 5 turnos atrás)
- Acumulación de ruido (3+ turnos con <10 caracteres)
- Repetición de herramientas (5+ llamadas mismas herramientas sin output)
- Confusión de memoria (mezclar contenido de sesión anterior)
- Compresión frecuente (2+ compresiones ejecutadas)

## Instalación

### Hermes Agent
```bash
# Activación manual
/auto-context

# Modo auto habilitado por defecto
```

### Claude Code / OpenClaw
```bash
# Via Skill marketplace o clon manual
git clone https://github.com/0xcjl/auto-context.git ~/.claude/skills/auto-context
```

## Uso

### Modo Manual
```
/auto-context
```

Salida:
```
🧠 Reporte de Salud del Contexto
  • 32 turnos, 1 deriva de tema, densidad media
  • Nivel: 🟡 NOISY
  • Sugerencia: Continuar, considerar /btw para nuevo tema
```

### Modo Auto
Se activa automáticamente cuando se detectan señales. Ejemplo:
- "La sesión es algo larga, ¿sugeriría /fork para mantener eficiencia?"

## Créditos

- **Original**: [lovstudio/auto-context](https://github.com/lovstudio/skills/tree/main/skills/lovstudio-auto-context)
- **Adaptación Hermes**: [0xcjl/auto-context](https://github.com/0xcjl/auto-context)
- **Investigación**: Papers ArXiv sobre gestión de contexto, psicología cognitiva

## Licencia

MIT
