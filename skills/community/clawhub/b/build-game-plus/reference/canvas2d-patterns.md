# Canvas2D Engine Patterns (2D games)

Pure Canvas2D, single HTML file, no imports. Same structural discipline as the
3D skill (CONSTANTS → DATA → STATE → FACTORIES → SYSTEMS → RENDER → LOOP).

## Boilerplate

```html
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>[Title]</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:#0d0d18; overflow:hidden; font-family:'Segoe UI',sans-serif; }
  #wrap { position:fixed; inset:0; display:grid; place-items:center; }
  canvas { image-rendering:auto; box-shadow:0 0 80px rgba(0,0,0,.6); }
  #hud { position:fixed; inset:0; pointer-events:none; z-index:10; }
</style></head>
<body><div id="wrap"><canvas id="game" width="1280" height="720"></canvas></div>
<div id="hud"></div>
<script>
// CONSTANTS first — every tunable here
// ...
</script></body></html>
```

## Fixed logical resolution + DPR scaling

```js
const W=1280, H=720, cvs=document.getElementById('game'), ctx=cvs.getContext('2d');
function fit(){
  const dpr=Math.min(devicePixelRatio||1,2), s=Math.min(innerWidth/W, innerHeight/H);
  cvs.style.width=(W*s)+'px'; cvs.style.height=(H*s)+'px';
  cvs.width=W*dpr; cvs.height=H*dpr; ctx.setTransform(dpr,0,0,dpr,0,0);
}
addEventListener('resize',fit); fit();
```

Draw everything in 1280×720 coordinates. Never read `canvas.width` for layout.

## Fixed-timestep loop

```js
const STEP=1/60; let acc=0, last=performance.now();
function frame(now){
  acc+=Math.min(0.25,(now-last)/1000); last=now;     // clamp: no spiral of death
  while(acc>=STEP){ update(STEP); acc-=STEP; }
  render();
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
```

## Procedural sprite factory (offscreen canvases)

Draw each entity ONCE to an offscreen canvas, then blit — cheap and lets you do
detail without per-frame cost:

```js
function makeSprite(w,h,drawFn){
  const c=document.createElement('canvas'); c.width=w; c.height=h;
  drawFn(c.getContext('2d'), w, h); return c;
}
const PLAYER = makeSprite(48,48,(g,w,h)=>{
  // body
  g.fillStyle=PAL.playerBody; roundRect(g,8,6,w-16,h-12,10); g.fill();
  // eyes, ears... describe the actual character here
});
```

`roundRect` helper: use `ctx.roundRect` (supported in Chrome 99+), else hand-roll.

Palettes: 3+ hues, 2+ luminance bands, and NOTHING below #1a1a1e for playfield
surfaces (same dark-scene rule as 3D — the verifier luminance check does not
care which engine you used).

## Entities + FSM

```js
const ents=[];
function spawn(type,x,y){ ents.push({type,x,y,vx:0,vy:0,hp:1,t:0,state:'idle',...DATA[type]}); }
function update(dt){
  for(const e of ents){ FSM[e.type]?.[e.state]?.(e,dt); e.x+=e.vx*dt; e.y+=e.vy*dt; }
}
const FSM={ grunt:{ idle:(e,dt)=>{ if(playerNear(e)) e.state='chase'; },
                    chase:(e,dt)=>{ steer(e,player,DATA.grunt.speed); if(playerFar(e))e.state='idle'; } } };
```

## Collision (AABB, pooled)

```js
function aabb(a,b){ return Math.abs(a.x-b.x)<(a.w+b.w)/2 && Math.abs(a.y-b.y)<(a.h+b.h)/2; }
```

Spatial partition (grid buckets) only when entity count > ~300. Below that,
brute force is faster than the partition overhead.

## Particles (pooled array, tiny but impactful)

```js
const MAXP=600, parts=[];                       // preallocate pool style:
function burst(x,y,n,color,spd=140){
  for(let i=0;i<n;i++){ if(parts.length>=MAXP) parts.shift();
    const a=Math.random()*Math.PI*2, s=spd*(0.3+Math.random()*0.7);
    parts.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,life:0.5+Math.random()*0.4,color}); }
}
function updateParts(dt){ for(let i=parts.length-1;i>=0;i--){ const p=parts[i];
  p.life-=dt; if(p.life<=0){ parts.splice(i,1); continue; }
  p.x+=p.vx*dt; p.y+=p.vy*dt; p.vy+=300*dt; } }
function drawParts(){ for(const p of parts){ ctx.globalAlpha=Math.min(1,p.life*2);
  ctx.fillStyle=p.color; ctx.fillRect(p.x-2,p.y-2,4,4); } ctx.globalAlpha=1; }
// per-type colors: hit=yellow-white, explode=orange, pickup=green, magic=purple
```

## Screen shake + hit flash (the juice)

```js
let shake=0, flash=0;
function addShake(n){ shake=Math.min(14,shake+n); }
function render(){
  ctx.save();
  if(shake>0){ ctx.translate((Math.random()*2-1)*shake,(Math.random()*2-1)*shake); shake*=0.88; if(shake<0.4)shake=0; }
  // draw world...
  ctx.restore();
  if(flash>0){ ctx.fillStyle=`rgba(255,60,60,${flash*=0.85})`; ctx.fillRect(0,0,W,H); }
}
```

## Procedural audio (Web Audio, same recipes as audio-patterns.md)

```js
const AC=new (window.AudioContext||window.webkitAudioContext)();
function sfx(freq=440,dur=0.1,type='square',vol=0.15,slide=0){
  const o=AC.createOscillator(), g=AC.createGain(), t=AC.currentTime;
  o.type=type; o.frequency.setValueAtTime(freq,t);
  if(slide) o.frequency.exponentialRampToValueAtTime(Math.max(30,freq+slide),t+dur);
  g.gain.setValueAtTime(vol,t); g.gain.exponentialRampToValueAtTime(0.001,t+dur);
  o.connect(g).connect(AC.destination); o.start(t); o.stop(t+dur);
}
// shoot: sfx(880,0.08,'square',0.12,-500);  hit: sfx(200,0.15,'sawtooth',0.2,-120);
// pickup: sfx(660,0.12,'triangle',0.15,+400); death: sfx(160,0.4,'sawtooth',0.25,-120);
// Resume AC on first input: addEventListener('pointerdown',()=>AC.resume(),{once:true});
```

## Backgrounds worth looking at (not flat fills)

- **Starfield**: pre-render to offscreen canvas once (400 stars, 2 layers), blit
  with parallax scroll offset.
- **Terrain**: pre-render full-width strip to an offscreen canvas (noise bumps,
  2-tone gradient, decorative scatter), blit per frame with camera offset.
- **Grid/Checker**: pre-render tile pattern via `createPattern`.

Pre-render everything static. Per-frame draw only entities + particles + HUD.

## Title screen

Same contract as 3D: game name, one-line objective, controls list, "Click to
Play". State machine `MODE = 'title' | 'play' | 'over'` — click/Enter on title
starts, game-over screen restarts on click, and `window.render_game_to_text()`
+ `window.advanceTime(ms)` debug hooks are REQUIRED so the verifier and future
iterations can drive the game.

## Common 2D pitfalls

- Forgetting `ctx.setTransform` reset after DPR scale → blurry everything.
- Drawing in CSS pixels but reading canvas.width (device px) → half-size game.
- Per-frame gradient creation → create gradients ONCE in CONSTANTS/init.
- `Math.hypot` in hot loops for 50+ entities → use squared distances.
- Unbounded arrays for bullets/particles → always pool or cap.
