"""
test_unified.py — 统一图引擎测试
用同一套算法生成所有图的示例
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from drawio_unified import generate_diagram

OUTPUT_DIR = r"C:\Users\sm001\WorkBuddy\2026-06-19-11-30-56"


# ================================================================
# 1. 网络拓扑 — 数据中心
# ================================================================
def gen_network():
    nodes = [
        {"id": "Core-SW1", "label": "Core-SW1"},
        {"id": "Core-SW2", "label": "Core-SW2"},
        {"id": "Dist-SW1", "label": "Dist-SW1"},
        {"id": "Dist-SW2", "label": "Dist-SW2"},
        {"id": "Dist-SW3", "label": "Dist-SW3"},
        {"id": "Access-SW1", "label": "Access-SW1"},
        {"id": "Access-SW2", "label": "Access-SW2"},
        {"id": "Firewall-1", "label": "Firewall-1"},
        {"id": "LoadBalancer", "label": "LoadBalancer"},
        {"id": "Web-Server-1", "label": "Web-Server-1"},
        {"id": "Web-Server-2", "label": "Web-Server-2"},
        {"id": "App-Server-1", "label": "App-Server-1"},
        {"id": "App-Server-2", "label": "App-Server-2"},
        {"id": "DB-Master", "label": "DB-Master"},
        {"id": "DB-Slave", "label": "DB-Slave"},
    ]
    edges = [
        {"from": "Core-SW1", "to": "Dist-SW1", "label": "40Gbps"},
        {"from": "Core-SW1", "to": "Dist-SW2", "label": "40Gbps"},
        {"from": "Core-SW2", "to": "Dist-SW2", "label": "40Gbps"},
        {"from": "Core-SW2", "to": "Dist-SW3", "label": "40Gbps"},
        {"from": "Dist-SW1", "to": "Access-SW1", "label": "10Gbps"},
        {"from": "Dist-SW1", "to": "Access-SW2", "label": "10Gbps"},
        {"from": "Dist-SW2", "to": "Access-SW1", "label": "10Gbps"},
        {"from": "Dist-SW2", "to": "Firewall-1", "label": "10Gbps"},
        {"from": "Dist-SW3", "to": "Access-SW2", "label": "10Gbps"},
        {"from": "Dist-SW3", "to": "LoadBalancer", "label": "10Gbps"},
        {"from": "Access-SW1", "to": "Web-Server-1", "label": "1Gbps"},
        {"from": "Access-SW1", "to": "Web-Server-2", "label": "1Gbps"},
        {"from": "Access-SW2", "to": "Web-Server-1", "label": "1Gbps"},
        {"from": "Access-SW2", "to": "Web-Server-2", "label": "1Gbps"},
        {"from": "Firewall-1", "to": "App-Server-1", "label": "1Gbps"},
        {"from": "Firewall-1", "to": "App-Server-2", "label": "1Gbps"},
        {"from": "LoadBalancer", "to": "App-Server-1", "label": "1Gbps"},
        {"from": "LoadBalancer", "to": "App-Server-2", "label": "1Gbps"},
        {"from": "Web-Server-1", "to": "App-Server-1", "label": "API"},
        {"from": "Web-Server-2", "to": "App-Server-2", "label": "API"},
        {"from": "App-Server-1", "to": "DB-Master", "label": "JDBC"},
        {"from": "App-Server-2", "to": "DB-Slave", "label": "JDBC"},
        {"from": "DB-Master", "to": "DB-Slave", "label": "Replication"},
    ]
    builder = generate_diagram(nodes, edges, "Data Center Network Topology")
    path = os.path.join(OUTPUT_DIR, "network_datacenter.drawio")
    builder.save(path)
    print(f"✅ network_datacenter.drawio")


# ================================================================
# 2. UML 类图 — 电商
# ================================================================
def gen_class():
    nodes = [
        {"id": "User", "label": "User"},
        {"id": "Order", "label": "Order"},
        {"id": "Product", "label": "Product"},
        {"id": "Payment", "label": "Payment"},
        {"id": "CartItem", "label": "CartItem"},
        {"id": "OrderItem", "label": "OrderItem"},
    ]
    edges = [
        {"from": "User", "to": "Order", "label": "1 → *"},
        {"from": "User", "to": "CartItem", "label": "1 → *"},
        {"from": "Order", "to": "OrderItem", "label": "1 → *"},
        {"from": "Product", "to": "OrderItem", "label": "1 → *"},
        {"from": "Product", "to": "CartItem", "label": "1 → *"},
        {"from": "Order", "to": "Payment", "label": "1 → 1"},
    ]
    builder = generate_diagram(nodes, edges, "UML Class Diagram - E-Commerce")
    path = os.path.join(OUTPUT_DIR, "class_diagram_ecommerce.drawio")
    builder.save(path)
    print(f"✅ class_diagram_ecommerce.drawio")


# ================================================================
# 3. ER 图 — 教育
# ================================================================
def gen_er():
    nodes = [
        {"id": "Lessons", "label": "Lessons"},
        {"id": "Courses", "label": "Courses"},
        {"id": "Students", "label": "Students"},
        {"id": "Enrollments", "label": "Enrollments"},
        {"id": "Users", "label": "Users"},
        {"id": "Reviews", "label": "Reviews"},
    ]
    edges = [
        {"from": "Lessons", "to": "Courses", "label": "1 → *"},
        {"from": "Courses", "to": "Enrollments", "label": "1 → *"},
        {"from": "Students", "to": "Enrollments", "label": "1 → *"},
        {"from": "Courses", "to": "Reviews", "label": "1 → *"},
        {"from": "Users", "to": "Reviews", "label": "1 → *"},
    ]
    builder = generate_diagram(nodes, edges, "ER Diagram - Education System")
    path = os.path.join(OUTPUT_DIR, "er_diagram_education.drawio")
    builder.save(path)
    print(f"✅ er_diagram_education.drawio")


# ================================================================
# 4. 思维导图 — AI技术栈
# ================================================================
def gen_mindmap():
    nodes = [
        {"id": "AI", "label": "AI Technology Stack"},
        {"id": "ML", "label": "Machine Learning"},
        {"id": "DL", "label": "Deep Learning"},
        {"id": "NLP", "label": "NLP"},
        {"id": "CV", "label": "Computer Vision"},
        {"id": "MLOps", "label": "MLOps"},
        {"id": "LLM", "label": "LLM / GenAI"},
        {"id": "ML1", "label": "Supervised"},
        {"id": "ML2", "label": "Unsupervised"},
        {"id": "ML3", "label": "Reinforcement"},
        {"id": "ML4", "label": "Semi-supervised"},
        {"id": "DL1", "label": "CNN"},
        {"id": "DL2", "label": "RNN/LSTM"},
        {"id": "DL3", "label": "Transformer"},
        {"id": "DL4", "label": "GAN"},
        {"id": "DL5", "label": "VAE"},
        {"id": "NLP1", "label": "Text Classification"},
        {"id": "NLP2", "label": "NER"},
        {"id": "NLP3", "label": "Machine Translation"},
        {"id": "NLP4", "label": "Sentiment Analysis"},
        {"id": "NLP5", "label": "Question Answering"},
        {"id": "CV1", "label": "Object Detection"},
        {"id": "CV2", "label": "Image Segmentation"},
        {"id": "CV3", "label": "Face Recognition"},
        {"id": "CV4", "label": "OCR"},
        {"id": "MO1", "label": "Pipeline Automation"},
        {"id": "MO2", "label": "Model Registry"},
        {"id": "MO3", "label": "Feature Store"},
        {"id": "MO4", "label": "Monitoring"},
        {"id": "LLM1", "label": "GPT / LLaMA"},
        {"id": "LLM2", "label": "RAG"},
        {"id": "LLM3", "label": "Fine-tuning"},
        {"id": "LLM4", "label": "Prompt Engineering"},
        {"id": "LLM5", "label": "Agent framework"},
    ]
    edges = [
        {"from": "AI", "to": "ML", "label": ""},
        {"from": "AI", "to": "DL", "label": ""},
        {"from": "AI", "to": "NLP", "label": ""},
        {"from": "AI", "to": "CV", "label": ""},
        {"from": "AI", "to": "MLOps", "label": ""},
        {"from": "AI", "to": "LLM", "label": ""},
        {"from": "ML", "to": "ML1", "label": ""},
        {"from": "ML", "to": "ML2", "label": ""},
        {"from": "ML", "to": "ML3", "label": ""},
        {"from": "ML", "to": "ML4", "label": ""},
        {"from": "DL", "to": "DL1", "label": ""},
        {"from": "DL", "to": "DL2", "label": ""},
        {"from": "DL", "to": "DL3", "label": ""},
        {"from": "DL", "to": "DL4", "label": ""},
        {"from": "DL", "to": "DL5", "label": ""},
        {"from": "NLP", "to": "NLP1", "label": ""},
        {"from": "NLP", "to": "NLP2", "label": ""},
        {"from": "NLP", "to": "NLP3", "label": ""},
        {"from": "NLP", "to": "NLP4", "label": ""},
        {"from": "NLP", "to": "NLP5", "label": ""},
        {"from": "CV", "to": "CV1", "label": ""},
        {"from": "CV", "to": "CV2", "label": ""},
        {"from": "CV", "to": "CV3", "label": ""},
        {"from": "CV", "to": "CV4", "label": ""},
        {"from": "MLOps", "to": "MO1", "label": ""},
        {"from": "MLOps", "to": "MO2", "label": ""},
        {"from": "MLOps", "to": "MO3", "label": ""},
        {"from": "MLOps", "to": "MO4", "label": ""},
        {"from": "LLM", "to": "LLM1", "label": ""},
        {"from": "LLM", "to": "LLM2", "label": ""},
        {"from": "LLM", "to": "LLM3", "label": ""},
        {"from": "LLM", "to": "LLM4", "label": ""},
        {"from": "LLM", "to": "LLM5", "label": ""},
    ]
    builder = generate_diagram(nodes, edges, "Mindmap - AI Technology Stack")
    path = os.path.join(OUTPUT_DIR, "mindmap_ai_stack.drawio")
    builder.save(path)
    print(f"✅ mindmap_ai_stack.drawio")


# ================================================================
# 5. 微服务架构图
# ================================================================
def gen_architecture():
    nodes = [
        {"id": "Gateway", "label": "API Gateway"},
        {"id": "Auth", "label": "Auth Service"},
        {"id": "UserSvc", "label": "User Service"},
        {"id": "OrderSvc", "label": "Order Service"},
        {"id": "ProductSvc", "label": "Product Service"},
        {"id": "PaymentSvc", "label": "Payment Service"},
        {"id": "Notification", "label": "Notification"},
        {"id": "DB-Main", "label": "Main Database"},
        {"id": "DB-Cache", "label": "Cache (Redis)"},
        {"id": "MQ", "label": "Message Queue"},
    ]
    edges = [
        {"from": "Gateway", "to": "Auth", "label": "verify"},
        {"from": "Gateway", "to": "UserSvc", "label": "route"},
        {"from": "Gateway", "to": "OrderSvc", "label": "route"},
        {"from": "Gateway", "to": "ProductSvc", "label": "route"},
        {"from": "Gateway", "to": "PaymentSvc", "label": "route"},
        {"from": "OrderSvc", "to": "MQ", "label": "publish"},
        {"from": "Notification", "to": "MQ", "label": "subscribe"},
        {"from": "UserSvc", "to": "DB-Main", "label": "CRUD"},
        {"from": "OrderSvc", "to": "DB-Main", "label": "CRUD"},
        {"from": "ProductSvc", "to": "DB-Main", "label": "CRUD"},
        {"from": "PaymentSvc", "to": "DB-Main", "label": "CRUD"},
        {"from": "ProductSvc", "to": "DB-Cache", "label": "cache"},
    ]
    builder = generate_diagram(nodes, edges, "Microservice Architecture")
    path = os.path.join(OUTPUT_DIR, "architecture_microservice.drawio")
    builder.save(path)
    print(f"✅ architecture_microservice.drawio")


# ================================================================
# 6. 组织结构图
# ================================================================
def gen_org():
    nodes = [
        {"id": "CEO", "label": "CEO"},
        {"id": "CTO", "label": "CTO"},
        {"id": "CFO", "label": "CFO"},
        {"id": "COO", "label": "COO"},
        {"id": "Eng", "label": "Engineering"},
        {"id": "PM", "label": "Product"},
        {"id": "Fin", "label": "Finance"},
        {"id": "Ops", "label": "Operations"},
        {"id": "Frontend", "label": "Frontend"},
        {"id": "Backend", "label": "Backend"},
        {"id": "DevOps", "label": "DevOps"},
        {"id": "QA", "label": "QA"},
        {"id": "Design", "label": "Design"},
        {"id": "Marketing", "label": "Marketing"},
        {"id": "HR", "label": "HR"},
    ]
    edges = [
        {"from": "CEO", "to": "CTO", "label": ""},
        {"from": "CEO", "to": "CFO", "label": ""},
        {"from": "CEO", "to": "COO", "label": ""},
        {"from": "CTO", "to": "Eng", "label": ""},
        {"from": "CTO", "to": "PM", "label": ""},
        {"from": "CFO", "to": "Fin", "label": ""},
        {"from": "COO", "to": "Ops", "label": ""},
        {"from": "Eng", "to": "Frontend", "label": ""},
        {"from": "Eng", "to": "Backend", "label": ""},
        {"from": "Eng", "to": "DevOps", "label": ""},
        {"from": "Eng", "to": "QA", "label": ""},
        {"from": "PM", "to": "Design", "label": ""},
        {"from": "Ops", "to": "Marketing", "label": ""},
        {"from": "Ops", "to": "HR", "label": ""},
    ]
    builder = generate_diagram(nodes, edges, "Organization Chart")
    path = os.path.join(OUTPUT_DIR, "tree_org_chart.drawio")
    builder.save(path)
    print(f"✅ tree_org_chart.drawio")


# ================================================================
if __name__ == "__main__":
    print("=" * 56)
    print("统一图引擎测试 —— 同一套算法生成全部图")
    print("=" * 56)
    print()

    gen_network()
    gen_class()
    gen_er()
    gen_mindmap()
    gen_architecture()
    gen_org()

    print()
    print("=" * 56)
    print("✅ 全部生成完毕！")

    # 打开预览
    import subprocess
    drawio_path = r"C:\Program Files\draw.io\draw.io.exe"
    if os.path.exists(drawio_path):
        for f in os.listdir(OUTPUT_DIR):
            if f.endswith(".drawio"):
                subprocess.Popen([drawio_path, os.path.join(OUTPUT_DIR, f)])
        print("📂 已在 draw.io 中打开全部图")
