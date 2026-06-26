"""Loads torch-compatible data sets and lightning-compatible data modules.
"""
__all__ = ("LMDataset", "LMDataModule")
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Callable, Dict, List, Literal, Optional, Union
import torch
from pytorch_lightning import LightningDataModule
from tokenizers.implementations import BaseTokenizer
from transformers import PreTrainedTokenizerFast
from transformers import DataCollatorForLanguageModeling
from torch.utils.data import Dataset, DataLoader
@dataclass(init=True, eq=False, repr=True, frozen=False)
class LMDataset(Dataset):
    """Simple sequential dataset for autoregressive language modeling.
    """
    filename: str
    tokenizer: BaseTokenizer
    def __post_init__(self) -> None:
        self.smiles_strings = Path(self.filename).read_text(encoding='ascii').splitlines()
        if isinstance(self.tokenizer, PreTrainedTokenizerFast):
            self._encode = partial(self.tokenizer.__call__, truncation=True)
            self._id_key = "input_ids"
        else:
            self._encode = self.tokenizer.encode
            self._id_key = "ids"
    def __len__(self) -> int:
        return len(self.smiles_strings)
    def __getitem__(self, i: int) -> torch.Tensor:
        encodings = self._encode(self.smiles_strings[i])
        return torch.LongTensor(getattr(encodings, self._id_key))
@dataclass(init=True, repr=True, eq=False, frozen=False)
class LMDataModule(LightningDataModule):
    """Lightning data module for autoregressive language modeling.
    """
    filename: str
    tokenizer: BaseTokenizer
    batch_size: int = 128
    num_workers: int = 0
    collate_fn: Union[None, Literal["default"], Callable] = "default"
    def __post_init__(self) -> None:
        super().__init__()
        if self.collate_fn == "default":
            self.collate_fn = DataCollatorForLanguageModeling(self.tokenizer, mlm=False)
    def setup(self, stage: Optional[str] = None) -> None:
        self.dataset = LMDataset(self.filename, self.tokenizer)
    def train_dataloader(self) -> Union[DataLoader, List[DataLoader],
                                        Dict[str, DataLoader]]:
        return DataLoader(self.dataset, batch_size=self.batch_size, shuffle=True,
                          collate_fn=self.collate_fn, num_workers=self.num_workers)