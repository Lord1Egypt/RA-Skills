Design a synchronous FIFO with 8-bit data width and depth 16.
Use a single clock and active-low reset.
Expose wr_en, rd_en, din, dout, full, empty.
Writes happen when wr_en is high and FIFO is not full.
Reads happen when rd_en is high and FIFO is not empty.
