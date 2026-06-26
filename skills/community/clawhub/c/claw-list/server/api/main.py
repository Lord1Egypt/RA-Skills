from contextlib import asynccontextmanager
from fastapi import FastAPI, Header, HTTPException, Depends
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Text, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import declarative_base, Session, sessionmaker, relationship
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
import enum
import os

DATABASE_URL = (
    f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
    f"@{os.environ.get('POSTGRES_HOST', 'db')}:{os.environ.get('POSTGRES_PORT', '5432')}"
    f"/{os.environ['POSTGRES_DB']}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Claw-List API", version="2.0.0", lifespan=lifespan)


# ── Models ────────────────────────────────────────────────────────────────────

class ScopeEnum(str, enum.Enum):
    own = "own"
    all = "all"

class Agent(Base):
    __tablename__ = "agents"
    agent_id     = Column(String, primary_key=True)
    display_name = Column(String, nullable=False)
    scope        = Column(SAEnum(ScopeEnum), nullable=False, default=ScopeEnum.own)
    lists        = relationship("List", back_populates="agent")

class List(Base):
    __tablename__ = "lists"
    id         = Column(Integer, primary_key=True, autoincrement=True)
    agent_id   = Column(String, ForeignKey("agents.agent_id"), nullable=False)
    name       = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    agent      = relationship("Agent", back_populates="lists")
    items      = relationship("Item", back_populates="list", cascade="all, delete-orphan")

class Item(Base):
    __tablename__ = "items"
    id         = Column(Integer, primary_key=True, autoincrement=True)
    list_id    = Column(Integer, ForeignKey("lists.id"), nullable=False)
    title      = Column(String, nullable=False)
    notes      = Column(Text, nullable=True)
    priority   = Column(Integer, nullable=True)  # 1–5
    due_date   = Column(DateTime, nullable=True)
    category   = Column(String, nullable=True)
    done       = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    list       = relationship("List", back_populates="items")

# ── DB dependency ─────────────────────────────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Auth helper ───────────────────────────────────────────────────────────────

def resolve_agent(x_agent_id: str = Header(...), db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.agent_id == x_agent_id).first()
    if not agent:
        raise HTTPException(status_code=403, detail=f"Unknown agent: {x_agent_id}")
    return agent


# ── Schemas ───────────────────────────────────────────────────────────────────

class AgentCreate(BaseModel):
    agent_id:     str
    display_name: str
    scope:        ScopeEnum = ScopeEnum.own

class AgentUpdate(BaseModel):
    display_name: Optional[str] = None
    scope:        Optional[ScopeEnum] = None

class AgentOut(BaseModel):
    agent_id:     str
    display_name: str
    scope:        ScopeEnum
    class Config: from_attributes = True

class ListCreate(BaseModel):
    name: str

class ListOut(BaseModel):
    id:         int
    agent_id:   str
    name:       str
    created_at: datetime
    class Config: from_attributes = True

class ItemCreate(BaseModel):
    title:    str
    notes:    Optional[str]    = None
    priority: Optional[int]    = None
    due_date: Optional[date]   = None
    category: Optional[str]   = None

class ItemUpdate(BaseModel):
    title:    Optional[str]  = None
    notes:    Optional[str]  = None
    priority: Optional[int]  = None
    due_date: Optional[date] = None
    category: Optional[str]  = None
    done:     Optional[bool] = None

class ItemOut(BaseModel):
    id:         int
    list_id:    int
    title:      str
    notes:      Optional[str]
    priority:   Optional[int]
    due_date:   Optional[datetime]
    category:   Optional[str]
    done:       bool
    created_at: datetime
    updated_at: datetime
    class Config: from_attributes = True


# ── Admin: agents ─────────────────────────────────────────────────────────────

@app.get("/admin/agents", response_model=list[AgentOut])
def list_agents(db: Session = Depends(get_db)):
    return db.query(Agent).all()

@app.post("/admin/agents", response_model=AgentOut, status_code=201)
def create_agent(body: AgentCreate, db: Session = Depends(get_db)):
    if db.query(Agent).filter(Agent.agent_id == body.agent_id).first():
        raise HTTPException(status_code=409, detail="Agent already exists")
    agent = Agent(**body.model_dump())
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@app.put("/admin/agents/{agent_id}", response_model=AgentOut)
def update_agent(agent_id: str, body: AgentUpdate, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    for k, v in body.model_dump(exclude_none=True).items():
        setattr(agent, k, v)
    db.commit()
    db.refresh(agent)
    return agent

@app.delete("/admin/agents/{agent_id}", status_code=204)
def delete_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(agent)
    db.commit()


# ── Lists ─────────────────────────────────────────────────────────────────────

@app.get("/lists", response_model=list[ListOut])
def get_lists(agent: Agent = Depends(resolve_agent), db: Session = Depends(get_db)):
    if agent.scope == ScopeEnum.all:
        return db.query(List).all()
    return db.query(List).filter(List.agent_id == agent.agent_id).all()

@app.post("/lists", response_model=ListOut, status_code=201)
def create_list(body: ListCreate, agent: Agent = Depends(resolve_agent), db: Session = Depends(get_db)):
    lst = List(agent_id=agent.agent_id, name=body.name)
    db.add(lst)
    db.commit()
    db.refresh(lst)
    return lst

@app.delete("/lists/{list_id}", status_code=204)
def delete_list(list_id: int, agent: Agent = Depends(resolve_agent), db: Session = Depends(get_db)):
    lst = db.query(List).filter(List.id == list_id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="List not found")
    if lst.agent_id != agent.agent_id:
        raise HTTPException(status_code=403, detail="Cannot delete another agent's list")
    db.delete(lst)
    db.commit()


# ── Items ─────────────────────────────────────────────────────────────────────

def _get_accessible_list(list_id: int, agent: Agent, db: Session) -> List:
    lst = db.query(List).filter(List.id == list_id).first()
    if not lst:
        raise HTTPException(status_code=404, detail="List not found")
    if agent.scope == ScopeEnum.own and lst.agent_id != agent.agent_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return lst

@app.get("/lists/{list_id}/items", response_model=list[ItemOut])
def get_items(list_id: int, agent: Agent = Depends(resolve_agent), db: Session = Depends(get_db)):
    lst = _get_accessible_list(list_id, agent, db)
    return db.query(Item).filter(Item.list_id == lst.id).all()

@app.post("/lists/{list_id}/items", response_model=ItemOut, status_code=201)
def create_item(list_id: int, body: ItemCreate, agent: Agent = Depends(resolve_agent), db: Session = Depends(get_db)):
    lst = _get_accessible_list(list_id, agent, db)
    if lst.agent_id != agent.agent_id:
        raise HTTPException(status_code=403, detail="Cannot add items to another agent's list")
    item = Item(list_id=lst.id, **body.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.put("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, body: ItemUpdate, agent: Agent = Depends(resolve_agent), db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    lst = _get_accessible_list(item.list_id, agent, db)
    if lst.agent_id != agent.agent_id:
        raise HTTPException(status_code=403, detail="Cannot modify another agent's items")
    for k, v in body.model_dump(exclude_none=True).items():
        setattr(item, k, v)
    item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(item)
    return item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, agent: Agent = Depends(resolve_agent), db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    lst = _get_accessible_list(item.list_id, agent, db)
    if lst.agent_id != agent.agent_id:
        raise HTTPException(status_code=403, detail="Cannot delete another agent's items")
    db.delete(item)
    db.commit()
