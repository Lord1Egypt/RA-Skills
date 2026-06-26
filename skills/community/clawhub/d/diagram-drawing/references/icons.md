# Icon Reference

## Compatibility Rule
**Never use `@import url()` for fonts** — rsvg-convert does not fetch external resources.
Use `<style>font-family: system-ui, Helvetica, sans-serif</style>` only.
**Never use external CDN URLs for icons** — use inline SVG paths.

---

## Semantic Shapes

### LLM / Model (double-border rounded rect)
```xml
<rect x="x" y="y" width="w" height="h" rx="10" fill="FILL" stroke="STROKE-OUTER" stroke-width="2.5"/>
<rect x="x+3" y="y+3" width="w-6" height="h-6" rx="8" fill="none" stroke="STROKE-INNER" stroke-width="0.8" opacity="0.5"/>
<text x="cx" y="cy-6" text-anchor="middle" font-size="14">⚡</text>
<text x="cx" y="cy+10" text-anchor="middle" fill="TEXT" font-size="13" font-weight="600">GPT-4o</text>
```

### Agent / Orchestrator (hexagon)
```xml
<!-- r=circumradius. For r=36: points at 36,0  18,31.2  -18,31.2  -36,0  -18,-31.2  18,-31.2 -->
<polygon points="cx,cy-r  cx+r*0.866,cy-r*0.5  cx+r*0.866,cy+r*0.5  cx,cy+r  cx-r*0.866,cy+r*0.5  cx-r*0.866,cy-r*0.5"
         fill="FILL" stroke="STROKE" stroke-width="1.5"/>
<text x="cx" y="cy+5" text-anchor="middle" fill="TEXT" font-size="12" font-weight="600">Agent</text>
```

### Vector Store (cylinder with rings)
```xml
<ellipse cx="cx" cy="top" rx="w/2" ry="w/6" fill="FILL" stroke="STROKE" stroke-width="1.5"/>
<rect x="cx-w/2" y="top" width="w" height="h" fill="FILL" stroke="none"/>
<line x1="cx-w/2" y1="top" x2="cx-w/2" y2="top+h" stroke="STROKE" stroke-width="1.5"/>
<line x1="cx+w/2" y1="top" x2="cx+w/2" y2="top+h" stroke="STROKE" stroke-width="1.5"/>
<ellipse cx="cx" cy="top+h*0.33" rx="w/2" ry="w/6" fill="none" stroke="STROKE" stroke-width="0.7" opacity="0.5"/>
<ellipse cx="cx" cy="top+h*0.66" rx="w/2" ry="w/6" fill="none" stroke="STROKE" stroke-width="0.7" opacity="0.5"/>
<ellipse cx="cx" cy="top+h" rx="w/2" ry="w/6" fill="FILL-DARK" stroke="STROKE" stroke-width="1.5"/>
```

### Memory (short-term, dashed border)
```xml
<rect x="x" y="y" width="w" height="h" rx="8"
      fill="FILL" stroke="STROKE" stroke-width="1.5" stroke-dasharray="6,3"/>
<text x="cx" y="cy-6" text-anchor="middle" fill="TEXT" font-size="10" opacity="0.7">MEMORY</text>
<text x="cx" y="cy+8" text-anchor="middle" fill="TEXT" font-size="13">Short-term</text>
```

### Tool / Function (rect with gear)
```xml
<rect x="x" y="y" width="w" height="h" rx="6" fill="FILL" stroke="STROKE" stroke-width="1.5"/>
<text x="cx" y="cy-4" text-anchor="middle" font-size="16">⚙</text>
<text x="cx" y="cy+12" text-anchor="middle" fill="TEXT" font-size="12">Tool Name</text>
```

### User / Human
```xml
<circle cx="cx" cy="cy-18" r="10" fill="FILL" stroke="STROKE" stroke-width="1.2"/>
<path d="M cx-14,cy+16 Q cx-14,cy-4 cx,cy-4 Q cx+14,cy-4 cx+14,cy+16"
      fill="FILL" stroke="STROKE" stroke-width="1.2"/>
<text x="cx" y="cy+30" text-anchor="middle" fill="TEXT" font-size="12">User</text>
```

### Browser / UI
```xml
<rect x="x" y="y" width="w" height="h" rx="6" fill="FILL" stroke="STROKE" stroke-width="1.5"/>
<rect x="x" y="y" width="w" height="20" rx="6" fill="FILL-DARK" stroke="none"/>
<rect x="x" y="y+14" width="w" height="6" fill="FILL-DARK"/>
<circle cx="x+12" cy="y+10" r="4" fill="#ef4444" opacity="0.8"/>
<circle cx="x+24" cy="y+10" r="4" fill="#f59e0b" opacity="0.8"/>
<circle cx="x+36" cy="y+10" r="4" fill="#10b981" opacity="0.8"/>
```

### Document / File
```xml
<path d="M x,y L x+w-12,y L x+w,y+12 L x+w,y+h L x,y+h Z"
      fill="FILL" stroke="STROKE" stroke-width="1.5"/>
<path d="M x+w-12,y L x+w-12,y+12 L x+w,y+12" fill="FILL-DARK" stroke="STROKE" stroke-width="1"/>
<line x1="x+8" y1="y+h*0.45" x2="x+w-8" y2="y+h*0.45" stroke="STROKE" stroke-width="1" opacity="0.5"/>
<line x1="x+8" y1="y+h*0.6" x2="x+w-8" y2="y+h*0.6" stroke="STROKE" stroke-width="1" opacity="0.5"/>
<line x1="x+8" y1="y+h*0.75" x2="x+w-16" y2="y+h*0.75" stroke="STROKE" stroke-width="1" opacity="0.5"/>
```

### Decision Diamond
```xml
<polygon points="cx,cy-hh  cx+hw,cy  cx,cy+hh  cx-hw,cy"
         fill="FILL" stroke="STROKE" stroke-width="1.5"/>
<text x="cx" y="cy+5" text-anchor="middle" fill="TEXT" font-size="12">Condition?</text>
```

### Swim Lane Container
```xml
<rect x="x" y="y" width="w" height="h" rx="6"
      fill="FILL" fill-opacity="0.04" stroke="STROKE" stroke-width="1" stroke-dasharray="6,4"/>
<text x="x+12" y="y+16" fill="LABEL-COLOR" font-size="10" font-weight="600" letter-spacing="0.06em">LAYER NAME</text>
```

---

## Product Icons (Circle Badge Pattern)

### AI / ML
| Product | Color | Badge |
|---------|-------|-------|
| OpenAI | `#10A37F` | `OAI` |
| Anthropic/Claude | `#D97757` | `Claude` |
| Google Gemini | `#4285F4` | `Gemini` |
| Meta LLaMA | `#0467DF` | `LLaMA` |
| Mistral | `#FF7000` | `Mistral` |
| Cohere | `#39594D` | `Cohere` |
| Groq | `#F55036` | `Groq` |
| Hugging Face | `#FFD21E` | `HF` |

### Vector DBs
| Product | Color | Badge |
|---------|-------|-------|
| Pinecone | `#1C1C2E` | `Pine` |
| Weaviate | `#FA0050` | `Wea` |
| Qdrant | `#DC244C` | `Qdrant` |
| Chroma | `#FF6B35` | `Chr` |
| Milvus | `#00A1EA` | `Milvus` |
| pgvector | `#336791` | `pgv` |

### Databases
| Product | Color |
|---------|-------|
| PostgreSQL | `#336791` |
| MySQL | `#4479A1` |
| MongoDB | `#47A248` |
| Redis | `#DC382D` |
| Elasticsearch | `#005571` |
| Neo4j | `#008CC1` |

### Messaging
| Product | Color |
|---------|-------|
| Kafka | `#231F20` |
| RabbitMQ | `#FF6600` |
| NATS | `#27AAE1` |

### Cloud/Infra
| Product | Color |
|---------|-------|
| AWS | `#FF9900` |
| GCP | `#4285F4` |
| Azure | `#0089D6` |
| Docker | `#2496ED` |
| Kubernetes | `#326CE5` |
| Vercel | `#000000` |

### Observability
| Product | Color |
|---------|-------|
| Grafana | `#F46800` |
| Prometheus | `#E6522C` |
| Datadog | `#632CA6` |
| LangSmith | `#1C3C3C` |
| Langfuse | `#6366F1` |

### AI Frameworks
| Product | Color | Badge |
|---------|-------|-------|
| LangChain | `#1C3C3C` | `LC` |
| LlamaIndex | `#8B5CF6` | `LI` |
| CrewAI | `#EF4444` | `Crew` |
| AutoGen | `#0078D4` | `AG` |
| DSPy | `#7C3AED` | `DSPy` |

### Badge Template
```xml
<circle cx="cx" cy="cy" r="22" fill="BRAND_COLOR"/>
<text x="cx" y="cy+5" text-anchor="middle" fill="white"
      font-size="10" font-weight="700">BADGE_TEXT</text>
<circle cx="cx" cy="cy" r="24" fill="none" stroke="BRAND_COLOR" stroke-width="1" opacity="0.4"/>
```

### Vector DB Badge Template
```xml
<!-- Cylinder shape -->
<ellipse cx="cx" cy="top" rx="40" ry="12" fill="FILL" stroke="STROKE" stroke-width="1.5"/>
<rect x="cx-40" y="top" width="80" height="50" fill="FILL" stroke="none"/>
<line x1="cx-40" y1="top" x2="cx-40" y2="top+50" stroke="STROKE" stroke-width="1.5"/>
<line x1="cx+40" y1="top" x2="cx+40" y2="top+50" stroke="STROKE" stroke-width="1.5"/>
<ellipse cx="cx" cy="top+50" rx="40" ry="12" fill="FILL_DARK" stroke="STROKE" stroke-width="1.5"/>
<!-- Badge overlay -->
<circle cx="cx" cy="top+25" r="16" fill="BRAND_COLOR"/>
<text x="cx" y="top+30" text-anchor="middle" fill="white" font-size="9" font-weight="700">BADGE</text>
```

---

## Arrow Marker Templates

```xml
<defs>
  <!-- Filled arrow -->
  <marker id="arrow-BLUE" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#2563eb"/>
  </marker>

  <!-- Open arrow (outline) -->
  <marker id="arrow-open" markerWidth="10" markerHeight="8"
          refX="9" refY="4" orient="auto">
    <path d="M 0 0 L 10 4 L 0 8" fill="none" stroke="COLOR" stroke-width="1.5"/>
  </marker>

  <!-- Circle dot (association) -->
  <marker id="dot" markerWidth="8" markerHeight="8"
          refX="4" refY="4" orient="auto">
    <circle cx="4" cy="4" r="3" fill="COLOR"/>
  </marker>
</defs>
```

## Sizing Guide

| Context | Size | Padding |
|---------|------|---------|
| Node badge | 28×28px circle | 10px |
| Standalone icon | 40×40px | 16px |
| Hero / central node | 56×56px | 20px |
| Small inline | 16×16px | 6px |
