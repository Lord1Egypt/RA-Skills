# Esquemas

## datos.json (entrada del motor)

```json
{
  "cuenta": { "handle": "tucuenta", "fuente": "panel «Ver insights» de Instagram, leído el 2026-09-15" },
  "proposito_mes": "Crecimiento",
  "piezas_mes": 12,
  "ventanas": null,
  "posts": [
    {
      "n": 1,
      "fecha": "2026-09-02",
      "url": "https://www.instagram.com/reel/CODE/",
      "portada": "portadas/01_CODE.jpg",
      "duracion_s": 42,
      "caption": "…",
      "transcript": "…",
      "sin_voz": false,
      "metricas": {
        "vistas": 13537, "pct_no_seguidores": 63.3,
        "likes": 385, "comentarios": 30, "guardados": 133, "compartidos": 40,
        "seguidores_nuevos": 3,
        "retencion_3s": null, "duracion_media": null,
        "visitas_perfil": null, "toques_enlace": null, "dms": null
      },
      "etiquetas": { "formato": "Comparación", "angulo": "Error común", "proposito": "Crecimiento" }
    }
  ]
}
```

- `n`: 1 = el más nuevo. `fecha` en AAAA-MM-DD.
- `ventanas`: `null` el primer mes (el motor parte 20 viejos / 10 nuevos). Desde el segundo mes: `{ "base": [n…], "mes": [n…] }`.
- `ventana.dias_publicando` (opcional): si la cuenta lleva más días publicando que lo que abarca el lote.
- Números crudos: `7479.5`, nunca `"7.479,5"`. Lo que no hay es `null`.

## resultado.json → calidadDatos (lo pone el motor)

`basicas: { con, total, faltan[] }` · `avanzadas[]`: `{ clave: retencion|perfil, nombre, filtro, captura, desbloquea, con, total, faltan[], prioridad[], estado: completo|parcial|sin-dato }` · `completa`.
Un filtro solo se lee si cada ventana tiene `min(5, mitad de la ventana)` Reels con el dato.

## resultado.json → conclusionesFijas (lo pone el motor)

`formato.estado` = repetir · candidato · sin-ganador, con `ganadores[]` ({ formato, oro, chatarra, veces, referencias, mediana }) y `matar[]`.
`anguloViral` y `anguloVenta`: `estado` = ganador · sin-ganador · sin-dato, `angulo`, `mediana`, `medianaCuenta`, `veces`, `arriba`, `fuerza` (patron · pista), `referencias`, `tabla` (top 5) y, en venta, `seguridad` = coronado · medido · proxy.
`medianas` = mediana del lote por columna: el informe arma con ella la meta de cada pieza.

## lectura.json (lo que redacta la IA)

```json
{
  "resumen": "Tu filtro tapado es el Alcance: …",
  "videos": { "1": { "gancho": "primera frase literal", "idea": "de qué va" } },
  "preguntas": [
    { "id": "p1", "tipo": "hipotesis", "pregunta": "¿…?", "porque": "…", "evidencia": [18, 29], "destino": "…" },
    { "id": "e1", "tipo": "encuesta", "pregunta": "Cuéntame con tus palabras…", "porque": "…" }
  ],
  "conclusiones_fijas": {
    "formato": { "texto": "por qué ganó el formato que eligió el motor", "evidencia": [29, 27] },
    "angulo_viral": { "angulo_especifico": "Curiosidad de cómo generar contenido viral en automático con Claude", "texto": "…", "evidencia": [29] },
    "angulo_venta": { "angulo_especifico": "Método paso a paso para que Claude te haga el trabajo pesado", "texto": "…", "evidencia": [4, 17] }
  },
  "conclusiones": [ { "titulo": "…", "texto": "…", "evidencia": [29, 30] } ],
  "aplicacion": {
    "calendario": [
      { "semana": 1, "dia": "Lun", "tema": "…", "formato": "…", "angulo": "Curiosidad", "proposito": "Crecimiento",
        "de_donde_sale": "REPETIR", "filtro_que_ataca": "1 Alcance",
        "angulo_exacto": "la frase del ángulo aplicada a este tema",
        "gancho": "primera frase literal", "texto_pantalla": "rótulo del segundo 1 (opcional)",
        "estructura": ["paso 1", "paso 2", "paso 3"],
        "cta": "Comenta PALABRA y …",
        "referencia": { "post": 29, "que_copiar": "el movimiento concreto que se copia de ese Reel" },
        "por_que": "…", "evidencia": [29] },
      { "semana": 2, "de_donde_sale": "APOSTAR", "formato": "Duelo de mentalidades", "…": "…",
        "referencia": { "biblioteca": "Duelo de mentalidades", "que_copiar": "…" } }
    ],
    "campana": null,
    "sin_campana": "…",
    "apuesta": { "formato": "…", "por_que": "…", "tasa_mediana": 0.21,
      "ganchos": { "A": "…", "B": "…", "C": "…", "D": "…" } },
    "esta_semana": ["…", "…", "…"]
  }
}
```
