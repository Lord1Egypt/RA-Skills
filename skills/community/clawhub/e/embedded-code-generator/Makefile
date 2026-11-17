# Makefile for embedded-code-generator self-check tests
#
# Usage:
#   make test    - build and run all tests (must be warning-free)
#   make clean   - remove build artifacts
#
# The CRC template is verified in both configurations (bit-by-bit and
# table-driven). The ring buffer full policy is a compile-time macro
# (RB_STRATEGY), so tests/test_ring_buffer.c is compiled twice into two
# separate test binaries.

CC     := gcc
CFLAGS := -std=c99 -Wall -Wextra -O0
TMPL   := templates
BUILD  := build

TARGETS := $(BUILD)/test_crc \
           $(BUILD)/test_crc_table \
           $(BUILD)/test_rb_reject \
           $(BUILD)/test_rb_overwrite \
           $(BUILD)/test_soft_i2c \
           $(BUILD)/test_spi_master \
           $(BUILD)/test_adc_avg_filter \
           $(BUILD)/test_fsm_framework \
           $(BUILD)/test_pi_controller \
           $(BUILD)/test_lowpass_filter \
           $(BUILD)/test_rs485_tc \
           $(BUILD)/test_svpwm \
           $(BUILD)/test_dma_ring \
           $(BUILD)/test_soft_timer \
           $(BUILD)/test_mini_shell \
           $(BUILD)/test_lite_assert \
           $(BUILD)/test_key_scan \
           $(BUILD)/test_key_scan_high

.PHONY: test clean

test: $(TARGETS)
	@echo "=== Running tests ==="
	./$(BUILD)/test_crc
	./$(BUILD)/test_crc_table
	./$(BUILD)/test_rb_reject
	./$(BUILD)/test_rb_overwrite
	./$(BUILD)/test_soft_i2c
	./$(BUILD)/test_spi_master
	./$(BUILD)/test_adc_avg_filter
	./$(BUILD)/test_fsm_framework
	./$(BUILD)/test_pi_controller
	./$(BUILD)/test_lowpass_filter
	./$(BUILD)/test_rs485_tc
	./$(BUILD)/test_svpwm
	./$(BUILD)/test_dma_ring
	./$(BUILD)/test_soft_timer
	./$(BUILD)/test_mini_shell
	./$(BUILD)/test_lite_assert
	./$(BUILD)/test_key_scan
	./$(BUILD)/test_key_scan_high
	@echo "=== ALL TESTS PASSED ==="

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/test_crc: tests/test_crc.c $(TMPL)/crc_utils.c $(TMPL)/crc_utils.h | $(BUILD)
	$(CC) $(CFLAGS) -I$(TMPL) $< $(TMPL)/crc_utils.c -o $@

$(BUILD)/test_crc_table: tests/test_crc.c $(TMPL)/crc_utils.c $(TMPL)/crc_utils.h | $(BUILD)
	$(CC) $(CFLAGS) -DCRC_USE_TABLE -I$(TMPL) $< $(TMPL)/crc_utils.c -o $@

$(BUILD)/test_rb_reject: tests/test_ring_buffer.c $(TMPL)/ring_buffer.c $(TMPL)/ring_buffer.h | $(BUILD)
	$(CC) $(CFLAGS) -DRB_STRATEGY=0 -I$(TMPL) $< $(TMPL)/ring_buffer.c -o $@

$(BUILD)/test_rb_overwrite: tests/test_ring_buffer.c $(TMPL)/ring_buffer.c $(TMPL)/ring_buffer.h | $(BUILD)
	$(CC) $(CFLAGS) -DRB_STRATEGY=1 -I$(TMPL) $< $(TMPL)/ring_buffer.c -o $@

$(BUILD)/test_soft_i2c: tests/test_soft_i2c.c $(TMPL)/soft_i2c.c $(TMPL)/soft_i2c.h | $(BUILD)
	$(CC) $(CFLAGS) -I$(TMPL) $< $(TMPL)/soft_i2c.c -o $@

$(BUILD)/test_spi_master: tests/test_spi_master.c $(TMPL)/spi_master.c $(TMPL)/spi_master.h | $(BUILD)
	$(CC) $(CFLAGS) -I$(TMPL) $< $(TMPL)/spi_master.c -o $@

$(BUILD)/test_adc_avg_filter: tests/test_adc_avg_filter.c $(TMPL)/adc_avg_filter.c $(TMPL)/adc_avg_filter.h | $(BUILD)
	$(CC) $(CFLAGS) -I$(TMPL) $< $(TMPL)/adc_avg_filter.c -o $@

$(BUILD)/test_fsm_framework: tests/test_fsm_framework.c $(TMPL)/fsm_framework.c $(TMPL)/fsm_framework.h | $(BUILD)
	$(CC) $(CFLAGS) -I$(TMPL) $< $(TMPL)/fsm_framework.c -o $@

# PI / low-pass / SVPWM tests use float math from libm
$(BUILD)/test_pi_controller: tests/test_pi_controller.c $(TMPL)/pi_controller.c $(TMPL)/pi_controller.h | $(BUILD)
	$(CC) $(CFLAGS) -I$(TMPL) $< $(TMPL)/pi_controller.c -o $@ -lm

$(BUILD)/test_lowpass_filter: tests/test_lowpass_filter.c $(TMPL)/lowpass_filter.c $(TMPL)/lowpass_filter.h | $(BUILD)
	$(CC) $(CFLAGS) -I$(TMPL) $< $(TMPL)/lowpass_filter.c -o $@ -lm

$(BUILD)/test_rs485_tc: tests/test_rs485_tc.c $(TMPL)/rs485_tc.c $(TMPL)/rs485_tc.h | $(BUILD)
	$(CC) $(CFLAGS) -I$(TMPL) $< $(TMPL)/rs485_tc.c -o $@

$(BUILD)/test_svpwm: tests/test_svpwm.c $(TMPL)/svpwm.c $(TMPL)/svpwm.h | $(BUILD)
	$(CC) $(CFLAGS) -I$(TMPL) $< $(TMPL)/svpwm.c -o $@ -lm

$(BUILD)/test_dma_ring: tests/test_dma_ring.c $(TMPL)/dma_ring.c $(TMPL)/dma_ring.h | $(BUILD)
	$(CC) $(CFLAGS) -I$(TMPL) $< $(TMPL)/dma_ring.c -o $@

$(BUILD)/test_soft_timer: tests/test_soft_timer.c $(TMPL)/soft_timer.c $(TMPL)/soft_timer.h | $(BUILD)
	$(CC) $(CFLAGS) -I$(TMPL) $< $(TMPL)/soft_timer.c -o $@

$(BUILD)/test_mini_shell: tests/test_mini_shell.c $(TMPL)/mini_shell.c $(TMPL)/mini_shell.h | $(BUILD)
	$(CC) $(CFLAGS) -I$(TMPL) $< $(TMPL)/mini_shell.c -o $@

$(BUILD)/test_lite_assert: tests/test_lite_assert.c $(TMPL)/lite_assert.c $(TMPL)/lite_assert.h | $(BUILD)
	$(CC) $(CFLAGS) -I$(TMPL) $< $(TMPL)/lite_assert.c -o $@

# Key scanner is verified in both polarities (KS_ACTIVE_LEVEL 0 / 1)
$(BUILD)/test_key_scan: tests/test_key_scan.c $(TMPL)/key_scan.c $(TMPL)/key_scan.h | $(BUILD)
	$(CC) $(CFLAGS) -I$(TMPL) $< $(TMPL)/key_scan.c -o $@

$(BUILD)/test_key_scan_high: tests/test_key_scan.c $(TMPL)/key_scan.c $(TMPL)/key_scan.h | $(BUILD)
	$(CC) $(CFLAGS) -DKS_ACTIVE_LEVEL=1u -I$(TMPL) $< $(TMPL)/key_scan.c -o $@

clean:
	rm -rf $(BUILD)
