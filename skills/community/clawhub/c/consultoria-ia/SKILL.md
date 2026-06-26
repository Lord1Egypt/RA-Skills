# Skill: Consultoría IA

**ID:** consultoria-ia  
**Versión:** 1.0.0  
**Autor:** Marcelo Bustos <mgbustos70@gmail.com>  
**Licencia:** CC-BY-NC-4.0  
**OpenClaw:** >=2026.4.0  

## Descripción
Sistema completo de consultoría en inteligencia artificial para PYMES. Incluye metodología McKinsey para diagnóstico, desarrollo de soluciones personalizadas, y seguimiento de ROI.

## Instalación
```bash
clawhub install consultoria-ia
```

## Uso
```bash
# En conversación con OpenClaw
/consultoria diagnosticar [empresa] [vertical]
/consultoria proponer-solucion [problema]
/consultoria calcular-roi [inversion] [beneficio-esperado]
```

## Comandos
- `diagnosticar` - Realiza diagnóstico McKinsey de negocio
- `proponer-solucion` - Diseña solución técnica de IA
- `calcular-roi` - Calcula ROI de inversión en IA
- `seguimiento` - Monitorea métricas de proyecto

## Configuración
```yaml
# En configuración de OpenClaw
agents:
  diagnosticador:
    model: claude-3-5-sonnet-20241022
    systemPrompt: "Eres consultor McKinsey especializado en IA..."
  
  desarrollador:
    model: gpt-4-turbo-preview
    systemPrompt: "Eres arquitecto técnico especializado en IA..."
  
  analista:
    model: claude-3-haiku-20240307
    systemPrompt: "Eres analista de datos especializado en ROI..."
```

## Archivos incluidos
- `RESUMEN-EJECUTIVO.md` - Documentación principal
- `flujo-entrevistas-mckinsey.md` - Flujo diagnóstico
- `flujo-desarrollo-soluciones.md` - Flujo desarrollo
- `agentes/` - Agentes especializados
- `templates/` - Plantillas reutilizables
- `checklists/` - Listas de verificación

## Requisitos
- OpenClaw 2026.4.0 o superior
- Acceso a modelos: Claude Sonnet, GPT-4, Claude Haiku
- Permisos: filesystem, memory, tools básicos

## Ejemplos
Ver `EJEMPLO-FERRETERIA.md` para caso práctico completo.

## Soporte
Issues: https://github.com/mgbustos/consultoria-ia-skill/issues  
Email: mgbustos70@gmail.com

## Changelog
### 1.0.0 (2026-04-13)
- Versión inicial
- Documentación completa
- 3 agentes especializados
- Templates y checklists
- Ejemplo práctico

---
**Publicado:** 2026-04-13  
**Estado:** Activo  
**Categoría:** business/consulting