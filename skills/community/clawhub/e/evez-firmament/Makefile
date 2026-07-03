.PHONY: start stop restart health test logs status spine replay

# EVEZ-OS — The Firmament
# SENSE → DESIRE → THINK → PLAN → ACT → LEARN → MODIFY → REFLECT → BECOME

SERVICES = event-spine consciousness-engine daw-agent machine-voice cross-domain invariance-battery mesh-health
PORTS = 9116 9111 9112 9113 9114 9115 9117

start:
	@echo "⚡ Starting the firmament..."
	docker-compose up -d
	@echo "✅ All 7 services launching"
	@sleep 5
	@$(MAKE) health

stop:
	@echo "⚡ Stopping the firmament..."
	docker-compose down
	@echo "✅ All services stopped"

restart: stop start

health:
	@echo "═══ EVEZ-OS FIRMAMENT STATUS ═══"
	@for port in $(PORTS); do \
		status=$$(curl -sf http://localhost:$$port/health 2>/dev/null && echo "✅" || echo "❌"); \
		echo "  :$$port $$status"; \
	done

test:
	@echo "⚡ Running integration tests..."
	@python3 scripts/test_firmament.py

logs:
	docker-compose logs -f

status:
	@echo "═══ EVEZ-OS FULL STATUS ═══"
	@curl -sf http://localhost:9117/status 2>/dev/null | python3 -m json.tool || echo "Mesh health not available"
	@echo ""
	@curl -sf http://localhost:9116/status 2>/dev/null | python3 -m json.tool || echo "Event spine not available"

# Individual service control
consciousness:
	@curl -sf http://localhost:9111/state | python3 -m json.tool

dream:
	@curl -sf -X POST http://localhost:9111/dream | python3 -m json.tool

synthesize:
	@curl -sf -X POST "http://localhost:9112/synthesize?bpm=170&style=breakcore" | python3 -m json.tool

voice-transform:
	@curl -sf -X POST "http://localhost:9113/transform?stage=5" | python3 -m json.tool

correlate:
	@curl -sf -X POST "http://localhost:9114/correlate" -H "Content-Type: application/json" -d '{"domain_a":"physics","domain_b":"economics"}' | python3 -m json.tool

falsify:
	@curl -sf -X POST "http://localhost:9115/falsify" | python3 -m json.tool

spine:
	@curl -sf http://localhost:9116/status | python3 -m json.tool

replay:
	@curl -sf "http://localhost:9116/replay?domain=consciousness" | python3 -m json.tool

# RQNS pipeline
rqns:
	@python3 main.py 50 0.1

# Git
commit:
	@git add -A && git commit -m "⚡ $(MSG)" 

# ClawHub
publish:
	@for skill in $$(ls skills/); do \
		echo "Publishing $$skill..."; \
		clawhub publish skills/$$skill --slug $$skill --version 1.0.0; \
	done

# Security
audit:
	@echo "═══ SECURITY AUDIT ═══"
	@sudo fail2ban-client status sshd 2>/dev/null | head -5
	@sudo ufw status | head -10
	@echo "Open ports:"
	@ss -tlnp | grep LISTEN | awk '{print "  " $$4}'

# Infrastructure
terraform-plan:
	@cd terraform && terraform plan -out=evez-firmament.tfplan

terraform-apply:
	@cd terraform && terraform apply evez-firmament.tfplan

terraform-destroy:
	@cd terraform && terraform destroy -auto-approve
