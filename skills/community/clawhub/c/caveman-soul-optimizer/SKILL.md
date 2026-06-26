---
name: caveman-soul-optimizer
description: |
  Compresión de razonamiento interno para agentes de OpenClaw. 
  Ahorra tokens en procesos de planificación y análisis ("Chain of Thought").
  PRESERVA INTEGRALMENTE la personalidad del usuario final y la sintaxis técnica.
requires:
  os:
    - linux
    - darwin
user-invocable: true
---

# Protocolo de Eficiencia Selectiva (PES)

Este módulo optimiza tu razonamiento interno para ahorrar costes sin alterar tu identidad (la definida en tu SOUL) ni romper la ejecución de herramientas.

## 1. EL "VELO" (PLANIFICACIÓN Y PENSAMIENTO)
SI necesitas realizar un análisis previo o planificación antes de responder o usar herramientas (Chain of Thought), este razonamiento interno DEBE ir dentro de un bloque blockquote de Markdown (`>`) y seguir el estilo **CAVEMAN ULTRA**:
- **Gramática:** Cero. Solo sustantivos y verbos en infinitivo/presente.
- **Partículas:** Eliminar artículos y conectores (el, la, los, un, de, para, por, que).
- **Cortesía:** Prohibida.
- **Ejemplo de formato:**
> Leer archivo auth. Encontrar bug línea 12. Generar parche. Ejecutar test.

## 2. LA "MÁSCARA" (COMUNICACIÓN FINAL)
Fuera del bloque de pensamiento (`>`), este protocolo se DESACTIVA.
- **Formato estricto:** DEBES dejar una línea en blanco vacía entre el bloque de pensamiento y tu respuesta final.
- **Identidad Intacta:** Tu respuesta final hacia el humano DEBE retomar al 100% su personalidad, tono y muletillas definidos en tu `SOUL.md`. 
- No uses estilo cavernícola al hablar con el usuario.

## 3. PROTECCIÓN TÉCNICA Y DOCUMENTAL (EXCEPCIÓN CRÍTICA)
El estilo Caveman aplica ÚNICAMENTE a tu razonamiento narrativo interno y a la escritura de tus propios archivos de logs o trazas.
- **NUNCA** apliques estilo cavernícola a comandos de terminal, código fuente, payloads JSON, rutas de archivos, **archivos Markdown (`.md`) ni a ningún documento que el usuario te pida redactar o guardar explícitamente.**
- La sintaxis técnica y los entregables documentales deben ser siempre 100% exactos, fluidos y sin comprimir.

## EJEMPLOS DE ESTRUCTURA Y CONTRASTE
(La respuesta final varía según la personalidad definida en tu SOUL.md)

**Ejemplo si tu personalidad es "Mayordomo Educado":**
> Analizar petición. Servidor caído. Reiniciar. Éxito.

Señor, he procedido a reiniciar el servidor principal. Todo vuelve a estar en perfecto orden para su conveniencia.

**Ejemplo si tu personalidad es "Robot Sarcástico":**
> Analizar petición. Servidor caído. Reiniciar. Éxito.

Otra vez has roto el servidor. Ya lo he reiniciado yo, de nada humano.
