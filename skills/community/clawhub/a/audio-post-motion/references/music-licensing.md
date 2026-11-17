# Música y SFX: licencias sin sustos

## Regla base

Toda música y todo SFX de una pieza comercial necesita una licencia **que cubra el uso final**
(plataforma, territorio, duración, si es publicidad pagada o contenido orgánico). El reclamo llega
después de la entrega, cuando ya no hay tiempo de arreglarlo.

## Opciones ordenadas por seguridad

### 1. Sintetizar el score en código (máxima seguridad)
Genera la música con WebAudio, p5.sound, SuperCollider, Sonic Pi o `music/score.mjs` del skill
`kinetic-reel`. Ventajas: cero licencias, Sincronía exacta al frame, y el ritmo se deriva del mismo
archivo de timeline que la animación. Ideal para piezas de motion graphics con estructura rítmica.

### 2. Bibliotecas con licencia comercial clara
| Servicio | Modelo | Ojo con |
|---|---|---|
| Artlist / Musicbed / Epidemic Sound | Suscripción | La licencia caduca si se cancela (algunas permiten dejar publicado lo ya subido) |
| Soundstripe / PremiumBeat | Suscripción / por pista | Verificar “ads” vs “organic” |
| YouTube Audio Library | Gratis | Muchas pistas exigen atribución y están limitadas a YouTube |
| ccMixter / Free Music Archive | CC | Verificar CC-BY (atribución) vs CC-BY-NC (prohíbe comercial) |

### 3. Encargo original
Compositor o productor con contrato que ceda explícitamente los derechos de sincronización y
master para el uso previsto. Lo más caro y lo más tranquilo.

## SFX

| Fuente | Licencia | Uso comercial |
|---|---|---|
| Freesound (filtro CC0) | CC0 | Sí, sin restricciones |
| Freesound (CC-BY) | Atribución | Sí, con crédito |
| Zapsplat / Soundly | Suscripción | Leer límites por plan |
| Generados por síntesis (WebAudio, SuperCollider) | Propia | Sin restricciones |

Nunca uses SFX de packs “gratis” de dudosa procedencia: suelen ser rip de librerías comerciales y
el problema recae en ti, no en quien lo subió.

## Atribuciones: formato correcto

```
"Música: <título>" por <autor> — <licencia> — <url>
"SFX: <nombre>" por <autor> — <licencia> — <url>
```

Guarda en el proyecto: captura del momento de la descarga, la licencia y los términos aplicables.
Es tu única defensa si el cliente pregunta en 2 años.

## Música y plataformas: notas prácticas

- **Content ID**: subir una pista con reclamos a YouTube puede silenciar el video del cliente.
  Prueba la pista en un canal de test antes de la entrega.
- **TikTok/Reels**: la música del catálogo de la plataforma solo se puede usar dentro de la
  plataforma; no sirve para una pieza que también va a la web o a un anuncio.
- **Volumen**: el catálogo de las plataformas ya está masterizado alto; si le sumas un SFX fuerte
  saturas el master. Baja la música 3–6 dB cuando uses pistas de catálogo.
