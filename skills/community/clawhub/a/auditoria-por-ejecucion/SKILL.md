---
name: auditoria-por-ejecucion
description: Usar cuando un repositorio, documento o informe declare una garantia que un gate deberia comprobar — "los tests pasan", "el deploy esta automatizado", "el panel muestra X", "esta publicado", "no hay vulnabilidades". Sirve para auditing de codigo de terceros, para revisar la propia documentacion del proyecto, y para no repetir la clase de fallo mas comun que existe en software: una afirmacion, un chequeo, y el hueco entre ambos. Medir ejecutando el comando; juzgar por codigo de salida y no por prosa. Nace de medir cuatro proyectos reales — alpha-beth-lab (validate_corpus.mjs imprimia "VERDICT: CORRUPT" y salia 0, y npm run verify:all pasaba entero con exit 0), GlobalCorp (README con 4 deploy stub, dos paneles de Grafana con metricas que el codigo nunca emite, scanners de seguridad con || true), Proyecto Sabermetria (claim-graph + observation-manifest + verification-economics) y Api openfootball (ledger con "Do not claim public marketplace approval without evidence"). Limites de confianza de los scripts incluidos: sin --yes nada se ejecuta (auditar_repo.mjs es dry-run; verificar_declaraciones.mjs omite el gate y sus detectores estaticos son solo lectura); el env del proceso hijo se sanitiza por defecto (sin KEY/TOKEN/SECRET/PASSWORD/CREDENTIAL/BEARER/AUTH) y --full-env es la renuncia explicita; ejecutar codigo de terceros solo en contexto desechable. This skill is intentionally Spanish-language: its target audience is Spanish-speaking, and all user-facing text is Spanish by design, not by omission.
---

# Auditoria por ejecucion

La prosa afirma. El codigo hace. Cuando los dos discrepan, el codigo gana.

Este skill existe porque los cuatro proyectos de donde salen todos fallaron de la misma manera: no mintieron por descuido, mintieron porque **nadie ejecuto el comando**. Un gate que imprime un veredicto negativo y sale con codigo 0 es peor que no tener gate: un `&&` y un CI lo leen como verde.

## Limites de confianza (leer antes de ejecutar)

Los dos scripts incluidos auditan repos de terceros y uno de ellos puede ejecutar codigo. Tres fronteras, en orden:

1. **Consentimiento explicito por corrida.** Sin `--yes`, `auditar_repo.mjs` NO ejecuta nada: imprime el plan (comando, destino, estado del env) y sale 0. `verificar_declaraciones.mjs` corre siempre sus detectores estaticos (100% lectura, sin `--gate` no ejecuta nada jamas); la ejecucion del `--gate` exige `--yes` y, sin ella, se omite con un aviso y el informe lo declara como OMITIDO.
2. **Entorno sanitizado por defecto.** El proceso hijo no ve ninguna variable cuyo nombre case con `KEY|TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL|BEARER|AUTH`. `--full-env` es la renuncia explicita: no usarla sobre codigo que no se ha leido.
3. **Contexto desechable.** Ejecutar gates de repos de terceros solo dentro de un worktree, contenedor o VM desechable — nunca en una maquina que guarde credenciales.

Nota de idioma: este skill es deliberadamente en español — su audiencia es hispanohablante y toda su interfaz (instrucciones, salidas de scripts, mensajes de error) está en español por diseño, no por omisión.

## 0. Orden de autoridad

Cuando dos fuentes discrepan, gana la de arriba:

1. **Comandos ejecutables y tests — evidencia primaria. Ejecutalos; no infieras de la prosa.**
2. El backlog/plan canonico del proyecto (registro, gates, matriz de brechas).
3. La documentacion tecnica (`audit`, `architecture`, `runbooks`).
4. Los informes de auditoria antiguos — **solo historico. Contienen metricas y estados contradictorios. Nunca citarlos como estado actual.**
5. El `README` — resumen, no fuente de verdad.

## 1. El codigo de salida es la verdad

Antes de reportar un gate como sano, correrlo y mirar el exit code. Imprimir `VERDICT: FAIL` y salir 0 es un defecto, no una excepcion.

Caso medido: `research/validate_corpus.mjs` de alpha-beth-lab imprimia `VERDICT: CORRUPT — DO NOT COMPUTE ELS ON THIS` sobre un corpus declarado corrupto, escribia el veredicto a disco y **no tenia ni una llamada a `process.exit`**. La cadena `npm run verify:all` (&& de 4 pasos) pasaba **entera con exit 0** mostrando los FAIL, y encima corria `SITE VERIFICATION: ALL CHECKS PASSED`. `assertClean` existia y estaba probada. El script nunca la invocaba.

Corolario en la otra direccion: un gate que sale con codigo 0 tambien puede estar roto si su unica comprobacion fuerte pasa sobre datos corruptos. Verificar que el gate falla cuando debe.

## 2. Tres estados, no dos

| Estado | Significa | Como se marca |
|---|---|---|
| **VERIFICADO** | Ejecutado. Con comando y codigo de salida. | ID + comando + exit code |
| **NO VERIFICADO** | No ejecutado. | `> **UNVERIFIED**` explicito |
| **REFUTADO** | Ejecutado y el resultado fue contrario. | Se conserva, **no se borra** |

El estado "no verificado" no es vergonzoso. Lo vergonzoso es llamarlo verificado.

## 3. Ledger de claims

Una fila por afirmacion. El coste se cifra en segundos o minutos.

```
| ID | Afirmacion | Fuente | Como se verifica | Coste | Decision | Resultado | Riesgo residual |
```

- **Decision** ∈ {verificar, diferir}. "Diferir" es legitimo cuando el riesgo del error es bajo — pero se escribe el riesgo residual, no se omite la fila.
- Resumen honesto del ledger: cuantos verificados, cuantos diferidos y por que, y **cual es el riesgo residual principal** ("la precision NO esta validada contra resultados reales" / "no existe edge validado").

## 4. Manifiesto de observaciones con independencia

Una fila por observacion, con la capa y el grupo que la produjo:

```
| ID | Fuente | Capa | Grupo | Ancla (file:line) | Observacion |
```

- **Capa**: codigo / ejecucion / lectura / config / output / docs externas.
- **Grupo**: quien produjo la observacion. Sirve para detectar que dos confirmaciones no son independientes.
- **Contamination notes** (seccion obligatoria): si el mismo observador hizo la lectura y la verificacion, se declara y se mitiga separando fases — leer ANTES de verificar por codigo.

Ejemplo textual: *"Grupo ejecucion y lectura ejecutados por el mismo observador — mitigado por separacion de fases"*.

## 5. Sospecha del harness primero

Cuando un verificador falla, la primera hipotesis es que **el verificador** esta roto, no lo verificado. Y documentar que el harness fue editado antes de producir el resultado final.

Caso medido: el reporte deia "MotorEstadistico crashea en todos los pares". El motor importado y corrido pasaba. El harness llamaba a `calcular_probabilidad_poisson`, un metodo inexistente.

## 6. Un grep que encuentra algo hay que leerlo

Falso positivo de seguridad clasico: `grep hardcoded_api_key` -> 2 hits que parecian claves reales. Eran `"your_api_key_here"` en docstrings. Antes de reportar un hallazgo de grep, **leer las lineas**.

## 7. Prueba el vecindario antes de acusar al sistema

Un bug verificado en un modulo no prueba que el sistema este roto. Medir el entorno distingue "un archivo mal" de "todo el sistema mal" — y esa distincion cambia por completo la prioridad del trabajo.

Caso medido: el predictor de un proyecto daba probabilidades que sumaban `1 + draw`. El otro motor daba `0.5193 + 0.2345 + 0.2462 = 1.0`. Un archivo mal, no el sistema.

## 8. Invariantes numericos: volumen, no juicio

Un invariante se demuestra con volumen. "Suma 1" verificado con 15.000 pares y 15.000 fallos es un hecho; con 3 ejemplos es una anécdota. Para reproducibilidad: contar usos de `np.random` y **seeds** — 37 usos y 0 seeds significa Monte Carlo no reproducible.

## 9. Cerrar una brecha es comportamiento + test

**Nunca marcar una brecha cerrada editando solo su linea de estado.** Cerrar = un cambio de comportamiento + un test que pase + un registro numerado en el plan. Un stub documentado como feature es una regresion.

Todo lo no implementado lleva un callout con `file:line`.

## 10. Afirmaciones separadas

**"Funcional" y "rentable" son afirmaciones separadas y se reportan por separado.** Lo mismo para: "funciona en local" / "esta desplegado"; "el gate existe" / "el gate cablea su veredicto al exit code"; "la API responde" / "la API responde con tus credenciales".

## 11. No afirmes lo externo sin evidencia

Si un tercero —proveedor, plataforma, marketplace, aprobacion— no ha aprobado, se reporta **pendiente/privado** nombrando el bloqueo externo. Nunca "aprobado".

Caso medido: un pipeline de trading con cuatro gates secuenciales, regla "[REGLA INQUEBRANTABLE: No avanzar sin pasar el anterior. NO EXCEPCIONES.]", y el trading en vivo **hard-bloqueado en el motor**, no solo en el CLI. La separacion entre "lo que puedo hacer" y "lo que me dejan hacer" es una feature de seguridad, no una limitacion.

## 12. No afirmes una restriccion sin medirla

Regla adoptada tras refutar la propia: *"never assert a network constraint you have not measured"*. Un allowlist de cuatro dominios derivado por intuicion; al medir, 28 de 64 hosts resolvian.

Igual con las cifras del propio estado: un snapshot es un snapshot. **Repetir la medicion antes de escalarla a diagnostico.** (Un RCODE 5 transitorio de DNS me llevo a "cuello de botella gravisimo" en una sesion; al repetir, ambos resolvers respondian y la API dava 200.)

## Checklist de una linea

> ¿Ejecute el comando? ¿Lei el exit code? ¿El gate falla cuando debe? ¿Separo verificado / no verificado / refutado? ¿Declaro la contaminacion de mis propias observaciones? ¿Cierro con comportamiento + test o solo con una linea de estado?