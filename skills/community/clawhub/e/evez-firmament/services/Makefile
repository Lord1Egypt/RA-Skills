.PHONY: start stop health test restart logs status

SERVICES_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PIDS_DIR := $(SERVICES_DIR)/.pids

SERVICES := \
	consciousness_engine:9111 \
	daw_agent:9112 \
	machine_voice:9113 \
	cross_domain:9114 \
	invariance:9115 \
	event_spine:9116 \
	mesh_health:9117

# ── Start all services ──────────────────────────────────────────────
start:
	@mkdir -p $(PIDS_DIR)
	@echo "Starting EVEZ-OS mesh..."
	@$(foreach svc, $(SERVICES), \
		$(eval NAME=$(word 1,$(subst :, ,$(svc)))) \
		$(eval PORT=$(word 2,$(subst :, ,$(svc)))) \
		echo "  Starting $(NAME) on :$(PORT)"; \
		python3 $(SERVICES_DIR)/$(NAME).py &; \
		echo $$! > $(PIDS_DIR)/$(NAME).pid; \
	)
	@sleep 1
	@echo "Mesh started. Use 'make health' to verify."

# ── Stop all services ───────────────────────────────────────────────
stop:
	@echo "Stopping EVEZ-OS mesh..."
	@$(foreach svc, $(SERVICES), \
		$(eval NAME=$(word 1,$(subst :, ,$(svc)))) \
		if [ -f $(PIDS_DIR)/$(NAME).pid ]; then \
			kill `cat $(PIDS_DIR)/$(NAME).pid` 2>/dev/null && echo "  Stopped $(NAME)" || true; \
			rm -f $(PIDS_DIR)/$(NAME).pid; \
		fi; \
	)
	@echo "Mesh stopped."

# ── Health check ────────────────────────────────────────────────────
health:
	@echo "EVEZ-OS Mesh Health:"
	@$(foreach svc, $(SERVICES), \
		$(eval NAME=$(word 1,$(subst :, ,$(svc)))) \
		$(eval PORT=$(word 2,$(subst :, ,$(svc)))) \
		RESULT=$$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$(PORT)/health 2>/dev/null || echo "000"); \
		if [ "$$RESULT" = "200" ]; then \
			printf "  ✅ %-25s :%s  ALIVE\n" "$(NAME)" "$(PORT)"; \
		else \
			printf "  ❌ %-25s :%s  DOWN (HTTP $$RESULT)\n" "$(NAME)" "$(PORT)"; \
		fi; \
	)

# ── Run integration tests ──────────────────────────────────────────
test:
	@echo "Running EVEZ-OS integration tests..."
	@python3 $(SERVICES_DIR)/test_mesh.py

# ── Restart ─────────────────────────────────────────────────────────
restart: stop start
	@echo "Mesh restarted."

# ── Logs ────────────────────────────────────────────────────────────
logs:
	@$(foreach svc, $(SERVICES), \
		$(eval NAME=$(word 1,$(subst :, ,$(svc)))) \
		if [ -f $(PIDS_DIR)/$(NAME).pid ]; then \
			echo "=== $(NAME) (PID: $$(cat $(PIDS_DIR)/$(NAME).pid)) ==="; \
		fi; \
	)

# ── Status (alias for health) ──────────────────────────────────────
status: health
